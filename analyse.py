import requests
import csv
import time
from requests.exceptions import ConnectionError, Timeout

# GitHub API Token (replace 'your_github_token' with your actual token)
TOKEN = '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'
headers = {"Authorization": f"token {TOKEN}"}


# Function to check the current rate limit and pause if needed
def check_rate_limit():
    rate_limit_url = "https://api.github.com/rate_limit"
    response = requests.get(rate_limit_url, headers=headers)
    rate_data = response.json()

    remaining_requests = rate_data['rate']['remaining']
    reset_time = rate_data['rate']['reset']

    if remaining_requests < 10:  # Pause if remaining requests are low
        reset_timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(reset_time))
        print(f"Approaching rate limit. Pausing until reset at {reset_timestamp}")
        time.sleep(60)  # Adjust sleep duration as needed
    else:
        print(f"Requests remaining: {remaining_requests}")


# Function to get Toronto users with over 100 followers
def get_toronto_users():
    url = "https://api.github.com/search/users"
    users = []
    page = 1
    per_page = 100  # Maximum number of items per page

    while True:
        params = {
            "q": "location:Toronto followers:>100",
            "per_page": per_page,
            "page": page
        }

        response = requests.get(url, headers=headers, params=params)

        # Check response status
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break

        data = response.json()

        # Check if data has 'items' key and if there are items in it
        if 'items' not in data or not data['items']:
            print("No more users found or query returned no results.")
            break

        users.extend(data['items'])
        page += 1
        print(f"Fetched {len(data['items'])} users from page {page}")

        # Check rate limit periodically
        check_rate_limit()

    return users


# Function to get detailed information for each user with retries
def get_user_details(user_login, retries=3, backoff=2):
    url = f"https://api.github.com/users/{user_login}"
    attempt = 0

    while attempt < retries:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an error for non-200 status codes
            data = response.json()

            # Clean up company names as specified
            if data.get('company'):
                data['company'] = data['company'].strip().lstrip('@').upper()

            # Format boolean and null values for consistency
            data['hireable'] = data['hireable'] if data['hireable'] is not None else ""
            data['email'] = data['email'] if data['email'] else ""
            data['bio'] = data['bio'] if data['bio'] else ""

            # Return the cleaned user details dictionary
            return {
                'login': data.get('login', ''),
                'name': data.get('name', ''),
                'company': data.get('company', ''),
                'location': data.get('location', ''),
                'email': data.get('email', ''),
                'hireable': data['hireable'],
                'bio': data['bio'],
                'public_repos': data['public_repos'],
                'followers': data['followers'],
                'following': data['following'],
                'created_at': data['created_at']
            }

        except (ConnectionError, Timeout) as e:
            attempt += 1
            print(f"Connection error on attempt {attempt}: {e}")
            if attempt < retries:
                time.sleep(backoff * attempt)  # Exponential backoff

    # If all retries fail, return None or handle the failure
    print(f"Failed to retrieve data for {user_login} after {retries} attempts.")
    return None


# Function to fetch details for all users and return as a list
def fetch_all_user_details(users):
    detailed_users = []
    for user in users:
        print(f"Fetching details for user: {user['login']}")
        user_detail = get_user_details(user['login'])
        if user_detail:  # Only append if the response was successful
            detailed_users.append(user_detail)
    return detailed_users


# Function to write user data to users.csv with utf-8 encoding
def write_users_csv(users_data):
    with open('users.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'login', 'name', 'company', 'location', 'email', 'hireable', 'bio',
            'public_repos', 'followers', 'following', 'created_at'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write each user's details
        for user in users_data:
            writer.writerow(user)

    print("users.csv has been created with detailed user information.")


# Function to get repositories for a user, up to 500
def get_user_repositories(user_login, max_repos=500):
    url = f"https://api.github.com/users/{user_login}/repos"
    repositories = []
    page = 1
    per_page = 100  # GitHub’s max items per page

    while len(repositories) < max_repos:
        params = {
            "per_page": per_page,
            "page": page,
            "sort": "pushed"
        }

        response = requests.get(url, headers=headers, params=params)

        # Check if response was successful
        if response.status_code != 200:
            print(f"Failed to fetch repositories for {user_login}: {response.status_code}")
            break

        data = response.json()

        # Stop if there are no more repositories
        if not data:
            break

        for repo in data:
            # Process each repository and add to the list
            license_name = repo.get('license', {}).get('key', '') if repo.get('license') else ""
            repositories.append({
                'login': user_login,
                'full_name': repo.get('full_name', ''),
                'created_at': repo.get('created_at', ''),
                'stargazers_count': repo.get('stargazers_count', 0),
                'watchers_count': repo.get('watchers_count', 0),
                'language': repo.get('language', ''),
                'has_projects': repo.get('has_projects', False),
                'has_wiki': repo.get('has_wiki', False),
                'license_name': license_name
            })

        # Increment the page count to get the next set of repositories
        page += 1

        # Check if we’ve reached the maximum number of repositories
        if len(repositories) >= max_repos:
            break

    return repositories


# Function to fetch repositories for all users
def fetch_all_repositories(users):
    all_repositories = []
    for user in users:
        print(f"Fetching repositories for user: {user['login']}")
        user_repos = get_user_repositories(user['login'])
        all_repositories.extend(user_repos)  # Add the user's repositories to the full list
    return all_repositories


# Function to write repository data to repositories.csv with utf-8 encoding
def write_repositories_csv(repositories_data):
    with open('repositories.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'login', 'full_name', 'created_at', 'stargazers_count',
            'watchers_count', 'language', 'has_projects', 'has_wiki', 'license_name'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write each repository's details
        for repo in repositories_data:
            writer.writerow(repo)

    print("repositories.csv has been created with detailed repository information.")


# Main script execution
if __name__ == "__main__":
    # Check rate limit
    check_rate_limit()

    # Fetch users from Toronto with over 100 followers (Step 2 and Step 3)
    toronto_users = get_toronto_users()
    detailed_users = fetch_all_user_details(toronto_users)
    write_users_csv(detailed_users)

    # Fetch repositories for each user (Step 4)
    repositories = fetch_all_repositories(detailed_users)
    write_repositories_csv(repositories)
