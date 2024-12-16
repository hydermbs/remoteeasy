from flask import Flask, request, render_template, jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from urllib.parse import urlencode
import threading
import logging
from datetime import datetime
import random
import sys

# Initialize Flask app
app = Flask(__name__)

# Configure the logging settings
logging.basicConfig(
    stream = sys.stdout,
    filename='process_log.txt',  # Log file name
    level=logging.INFO,          # Default log level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log message format
)

def log_process(message, level='INFO'):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if level.upper() == 'INFO':
        logging.info(f"{current_time} - {message}")
    elif level.upper() == 'WARNING':
        logging.warning(f"{current_time} - {message}")
    elif level.upper() == 'ERROR':
        logging.error(f"{current_time} - {message}")
    else:
        raise ValueError("Invalid log level. Use 'INFO', 'WARNING', or 'ERROR'.")

def open_url(url):
    user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36']
    session = requests.Session()
    headers = {'User-Agent': random.choice(user_agents)}
    response = session.get(url, headers=headers,timeout=10)
    response.raise_for_status()
    return response.text
    
def extract_data_remoteyeah(num):
    url = f'https://remoteyeah.com/?page={num}'
    response = open_url(url)
    soup = bs(response,'html.parser')
    big_box = soup.find_all('div',{'class':"gap-2 md:gap-4 p-4 md:p-8"})
    job_list = []
    for box in big_box:
        a = box.find('a')
        job_name = a.text.replace('\n',"")
        job_url = a.get('href')
        company = box.find('span',{"class":"font-semibold text-text-base leading-none mt-1"}).text
        dict_1 = {'Job_Name':job_name,
                'Job_url':job_url,
                'Company':company}
        job_list.append(dict_1)
    return job_list

def get_data_remotetrove(page):
  form_data = {
    "lang": "",
    "search_keywords": "",
    "search_location": "",
    "search_categories": [],
    "filter_job_type": [
      "freelance",
      "full-time",
      "internship",
      "part-time",
      "temporary",
      ""
    ],
    "per_page": 40,
    "orderby": "featured",
    "order": "DESC",
    "job_types": "",
    "page": f'{page}',
    "featured": "",
    "filled": "",
    "list_layout": "grid",
    "remote_position": "",
    "show_pagination": False,}
  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
      "Accept": "application/json, text/plain, */*"
  }
  encoded_data = urlencode(form_data, doseq=True)
  response = requests.post('https://remotetrove.com/jm-ajax/get_listings/',headers=headers,data=encoded_data)
  return response.json()

def extract_data_remotetrove(result):
  big_box = result['html']
  soup = bs(big_box,'html.parser')
  name_element = soup.find_all('li')
  job_list = []
  for i in name_element:
    verify = i.get('data-company')
    if verify:
      job_name = i.find('h4').text
      job_url = i.find('a').get('href')
      company = i.find('h3').text.replace('\n',"")
      dict_1 = {'Job_Name':job_name,
              'Job_url':job_url,
              'Company':company}
      job_list.append(dict_1)
  return job_list

def extract_remote(search,num):
    url = f'https://remote.com/jobs/all?query={search}&page={num}'
    response = open_url(url)
    soup = bs(response,'html.parser')

    big_box = soup.find_all('article',{"class":"sc-506be909-0 sc-31ccc88a-1 caZBsO fDTnCW"})
    job_list = []
    for box in big_box:
        job_name = box.find('span',{'class':"sc-a6d70f3d-0 fsvfbz"}).text
        job_url = box.find('a').get('href')
        company = box.find('span',{'class':"sc-a6d70f3d-0 cWvlWe"}).text
        dict_1 = {'Job_Name':job_name,
                    'Job_url':f"https://remote.com{job_url}",
                    'Company':company}
        job_list.append(dict_1)
    return job_list

def remote_yeah():
    jobs_list = []
    for i in range(1,10):
        data = extract_data_remoteyeah(i)
        jobs_list.extend(data)
        log_process(data)
    return jobs_list

def remotetrove():
    jobs_list = []
    for i in range(1,6):
        result = get_data_remotetrove(i)
        data = extract_data_remotetrove(result)
        jobs_list.extend(data)
    return jobs_list

def weworkremotely(search):
    url = f'https://weworkremotely.com/remote-jobs/search?term={search}'
    response = open_url(url)
    soup = bs(response,'html.parser')
    big_box = soup.find_all('li',{"class":"feature"})
    job_list = []
    for i in big_box:
        job_name = i.find('span',{"class":"title"}).text
        element_url = i.find_all('a')
        job_url = element_url[1].get('href')
        company = i.find('span',{'class':"company"}).text
        dict_1 = {'Job_Name':job_name,
                'Job_url':f"https://weworkremotely.com{job_url}",
                'Company':company}
        job_list.append(dict_1)
    return job_list

def remote(search):
    num = 1
    jobs_list =[]
    while True:
        data = extract_remote(search,num)
        if not data:
            log_process('No More data')
            break
        jobs_list.extend(data)
        num+=1
    return jobs_list

def fetch_all(search):
    shared_job = []
    lock = threading.Lock()
    def fetch_remote_yeah():
        result = remote_yeah()
        with lock:
            shared_job.extend(result)
    def fetch_remotetrove():
        result = remotetrove()
        with lock:
            shared_job.extend(result)
    def fetch_weworkremotely():
        result = weworkremotely(search)
        with lock:
            shared_job.extend(result)
    def fetch_remote():
        result = remote(search)
        with lock:
            shared_job.extend(result)

    thread_1 = threading.Thread(target=fetch_remote_yeah)
    thread_2 = threading.Thread(target=fetch_remotetrove)
    thread_3 = threading.Thread(target=fetch_weworkremotely)
    thread_4 = threading.Thread(target=fetch_remote)

    thread_1.start()
    thread_2.start()
    thread_3.start()
    thread_4.start()

    thread_1.join()
    thread_2.join()
    thread_3.join()
    thread_4.join()

    return shared_job

def convert_to_df(data):
    df = pd.DataFrame(data)
    if 'Job_url' in df.columns:
        # Create clickable links for the Job_url column
        df['Job_url'] = df['Job_url'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')
    return df



@app.route('/')
@cross_origin()
def search_page():
    return render_template('index.html')

@app.route('/fetch_jobs', methods=['GET'])
@cross_origin()
def fetch_jobs():
    search = request.args.get('search', '')
    data = fetch_all(search)
    df = convert_to_df(data)
    filtered = df[df['Job_Name'].str.contains(search, case=False, na=False)]
    return render_template(
        'results.html',
        tables=[filtered.to_html(classes='data', escape=False, index=False, header=True)], 
        titles=filtered.columns.values
    )
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
