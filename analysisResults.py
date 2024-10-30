import pandas as pd
from scipy.stats import pearsonr, linregress
import numpy as np

# Load datasets
users = pd.read_csv("users.csv", parse_dates=["created_at"])
repos = pd.read_csv("repositories.csv", parse_dates=["created_at"])

# 1. Top 5 users by followers
top_followers = users.nlargest(5, 'followers')['login'].tolist()
print("Top 5 users by followers:", ', '.join(top_followers))

# 2. Earliest registered users
earliest_users = users.sort_values('created_at').head(5)['login'].tolist()
print("Earliest registered users:", ', '.join(earliest_users))

# 3. Most popular licenses
popular_licenses = repos['license_name'].value_counts().index[:3].tolist()
print("Most popular licenses:", ', '.join(popular_licenses))

# 4. Most common company
common_company = users['company'].mode()[0]
print("Most common company:", common_company)

# 5. Most popular programming language
popular_language = repos['language'].mode()[0]
print("Most popular language:", popular_language)

# 6. Second most popular language for users who joined after 2020
post_2020_users = users[users['created_at'] > '2020-01-01']['login']
post_2020_repos = repos[repos['login'].isin(post_2020_users)]
second_popular_language = post_2020_repos['language'].value_counts().index[1]
print("Second most popular language after 2020:", second_popular_language)

# 7. Language with highest average stars
language_avg_stars = repos.groupby('language')['stargazers_count'].mean()
highest_avg_stars_language = language_avg_stars.idxmax()
print("Language with highest average stars:", highest_avg_stars_language)

# 8. Top 5 in leader strength (followers / (1 + following))
users['leader_strength'] = users['followers'] / (1 + users['following'])
top_leader_strength = users.nlargest(5, 'leader_strength')['login'].tolist()
print("Top 5 in leader strength:", ', '.join(top_leader_strength))

# 9. Correlation between followers and public repos
followers_repos_corr = users['followers'].corr(users['public_repos']).round(3)
print("Correlation between followers and public repos:", followers_repos_corr)

# 10. Regression slope of followers on public repos
slope_followers_repos = linregress(users['public_repos'], users['followers']).slope.round(3)
print("Slope of followers on public repos:", slope_followers_repos)

# 11. Correlation between projects and wiki enabled
projects_wiki_corr = repos['has_projects'].corr(repos['has_wiki']).round(3)
print("Correlation between projects and wiki enabled:", projects_wiki_corr)

# 12. Difference in following between hireable and non-hireable users
avg_following_hireable = users[users['hireable'] == True]['following'].mean()
avg_following_nonhireable = users[users['hireable'] == False]['following'].mean()
following_difference = (avg_following_hireable - avg_following_nonhireable).round(3)
print("Difference in following (hireable vs. non-hireable):", following_difference)

# 13. Regression slope of followers on bio word count
users['bio_word_count'] = users['bio'].fillna('').apply(lambda x: len(x.split()))
bio_followers_slope = linregress(users['bio_word_count'], users['followers']).slope.round(3)
print("Slope of followers on bio word count:", bio_followers_slope)

# 14. Users with most weekend-created repositories
repos['weekday'] = repos['created_at'].dt.weekday
weekend_repos = repos[repos['weekday'] >= 5]
weekend_repo_counts = weekend_repos['login'].value_counts().head(5).index.tolist()
print("Users with most weekend-created repos:", ', '.join(weekend_repo_counts))

# 15. Email sharing among hireable users
hireable_with_email = users[users['hireable'] == True]['email'].notnull().mean()
nonhireable_with_email = users[users['hireable'] == False]['email'].notnull().mean()
email_hireable_difference = (hireable_with_email - nonhireable_with_email).round(3)
print("Difference in email sharing (hireable vs. non-hireable):", email_hireable_difference)

# 16. Most common surname
# Extract surname only if there's at least one word in the name
users['surname'] = users['name'].fillna('').apply(lambda x: x.split()[-1] if x.strip() else "")
most_common_surname = users['surname'].value_counts()

# List most common surname(s), in alphabetical order if there's a tie
top_surnames = ', '.join(most_common_surname[most_common_surname == most_common_surname.max()].index.sort_values())
print("Most common surname:", top_surnames)
