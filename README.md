# Remote Easy 

A simple Flask application designed to help you find remote jobs by extracting data from popular job boards. The application displays only the latest relevant jobs based on your specified keywords, allowing you to save time and focus on what matters—finding your dream remote job!  

## Features  
- **Multi-platform Integration**: Fetches remote job listings from:
  - Remote Yeah  
  - Remote Trove  
  - We Work Remotely  
  - Remote.com  
- **Keyword Search**: Search for jobs using specific keywords.  
- **Latest Jobs Only**: Shows only the newest and most relevant job postings.  
- **CSV Download**: Download the job listings as a CSV file for offline access.  
- **Direct Application Links**: Click the provided link to directly apply for a job.  

## Hosted Application  
The app is hosted on AWS (EC2 instance) and is accessible via HTTP.  

🔗 **Access the app here**: [http://13.49.46.67/](http://13.49.46.67/)  

## Requirements  
- Python 3.x  
- Flask  
- Requests  
- Pandas  

## Installation  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/hydermbs/remoteeasy.git  
   cd remoteeasy 
   ```  

2. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. Run the application:  
   ```bash  
   python app.py  
   ```  

4. Open the application in your browser:  
   ```  
   http://127.0.0.1:5000  
   ```  

## How It Works  
1. Enter a keyword to search for remote jobs (e.g., "data engineer," "developer").  
2. The app scrapes job postings from supported platforms.  
3. View the results on a single page with direct application links.  
4. Download the results as a CSV file if needed.  

## Future Enhancements  
- Add more job platforms for broader search coverage.  
- Implement HTTPS for secure browsing.  
- Introduce user authentication for personalized features.  
- Add filters like job type, company, and location.  

## Feedback  
Your feedback and suggestions are invaluable! Feel free to open an issue or submit a pull request for improvements.  

---  

Let’s simplify remote job hunting! 🌍💼  

