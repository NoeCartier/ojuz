import requests
from bs4 import BeautifulSoup
from datetime import datetime
import db

def update_submissions(registered_users, start_id=999999999):
    """
    Fetch all submissions for registered users from the OJ website.

    Parameters:
        registered_users (list): A list of usernames registered in the database.
        start_id (int): The starting submission ID for pagination.

    Returns:
        list: A list of dictionaries containing submission details for registered users.
    """
    stop_id = db.get_variable_value("stop_id")  # Get the stop_id from the database
    new_stop_id = stop_id
    base_url = "https://oj.uz/submissions?direction=down&id="
    submissions = []
    current_id = start_id
    while True:
        # Fetch the page
        url = f"{base_url}{current_id}"
        response = requests.get(url)
        
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from {url}. HTTP Status Code: {response.status_code}")
        print(f"Fetching submissions from {url}")
        soup = BeautifulSoup(response.text, 'html.parser')
        table_rows = soup.find_all('tr')
        for row in table_rows:
            columns = row.find_all('td')
            if len(columns) < 6:  # Ensure it is a valid row with enough columns
                continue
            html_snippet = columns[1]
            timestamp = None
            timestamp_span = html_snippet.find('span', {'class': 'render-timestamp'})
            if timestamp_span and 'data-timestamp-iso' in timestamp_span.attrs:
                datetime_iso = timestamp_span['data-timestamp-iso']
                datetime_obj = datetime.fromisoformat(datetime_iso.replace('Z', '+00:00'))
                timestamp = int(datetime_obj.timestamp())
                                
            submission_id = int(columns[0].text.strip())
            username = columns[2].text.strip()
            problem_name = columns[3].text.strip()
            language = columns[4].text.strip()
            fraction = columns[5].text.strip()
            if(submission_id <= stop_id):
                break
            score = 0.0
            # Check if the fraction is in the format "XX / XX"

            # Update current_id to the last seen submission ID
            current_id = submission_id

            if "queue" in fraction or "Running" in fraction:
                continue

            if " / " in fraction:
                    numerator, denominator = map(float, fraction.split(" / "))
                    score = round(numerator / denominator, 6)

            if new_stop_id == stop_id:  
                new_stop_id = submission_id

            print([submission_id, timestamp, username, problem_name, language, score])
            #timestamp = datetime.strptime(submission_time, "%Y-%m-%d %H:%M:%S").timestamp()

            # Check if the username is in the list of registered users
            if username in registered_users:
                submissions.append([submission_id, timestamp, username, problem_name, language, score])

        
        # Break if we reach the end of submissions
        if submission_id <= stop_id:
            break
    # Update the stop_id in the database
    db.update_variable_value("stop_id", new_stop_id)
    
    return submissions