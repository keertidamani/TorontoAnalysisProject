import pandas as pd
from scipy.stats import linregress

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
# Counts license occurrences and extracts the top 3 licenses by popularity
popular_licenses = repos['license_name'].value_counts().index[:3].tolist()
print("Most popular licenses:", ', '.join(popular_licenses))

# 4. Most common company
# Identifies the most frequent company among users
common_company = users['company'].mode()[0]
print("Most common company:", common_company)

# 5. Most popular programming language
# Finds the language that appears most frequently in repos
popular_language = repos['language'].mode()[0]
print("Most popular language:", popular_language)

# 6. Second most popular language for users who joined after 2020
# Filters for users who joined after 2020 and identifies the second most popular language in their repos
post_2020_users = users[users['created_at'] > '2020-01-01']['login']
post_2020_repos = repos[repos['login'].isin(post_2020_users)]
second_popular_language = post_2020_repos['language'].value_counts().index[1]
print("Second most popular language after 2020:", second_popular_language)

# 7. Language with highest average stars
# Groups repos by language and calculates average stars, then selects the language with the highest average
language_avg_stars = repos.groupby('language')['stargazers_count'].mean()
highest_avg_stars_language = language_avg_stars.idxmax()
print("Language with highest average stars:", highest_avg_stars_language)

# 8. Top 5 in leader strength (followers / (1 + following))
# Calculates a "leader strength" metric and selects the top 5 users based on this value
users['leader_strength'] = users['followers'] / (1 + users['following'])
top_leader_strength = users.nlargest(5, 'leader_strength')['login'].tolist()
print("Top 5 in leader strength:", ', '.join(top_leader_strength))

# 9. Correlation between followers and public repos
# Computes the correlation coefficient between followers and public repositories
followers_repos_corr = users['followers'].corr(users['public_repos']).round(3)
print("Correlation between followers and public repos:", followers_repos_corr)

# 10. Regression slope of followers on public repos
# Performs linear regression to estimate followers' increase per additional repository
slope_followers_repos = linregress(users['public_repos'], users['followers']).slope.round(3)
print("Slope of followers on public repos:", slope_followers_repos)

# 11. Correlation between projects and wiki enabled
# Ensures has_projects and has_wiki are binary values and computes their correlation
repos['has_projects'] = repos['has_projects'].fillna(False).astype(int)
repos['has_wiki'] = repos['has_wiki'].fillna(False).astype(int)
projects_wiki_corr = repos['has_projects'].corr(repos['has_wiki']).round(3)
print("Correlation between projects and wiki enabled:", projects_wiki_corr)

# 12. Difference in following between hireable and non-hireable users
# Compares the average following count of hireable vs. non-hireable users
users['hireable'] = users['hireable'].fillna(False)
avg_following_hireable = users[users['hireable'] == True]['following'].mean()
avg_following_nonhireable = users[users['hireable'] == False]['following'].mean()
following_difference = (avg_following_hireable - avg_following_nonhireable).round(3)
print("Difference in following (hireable vs. non-hireable):", following_difference)

# 13. Regression slope of followers on bio word count
# Counts words in user bios and uses regression to calculate the impact on followers
users_with_bios = users[users['bio'].notnull()].copy()
users_with_bios['bio_word_count'] = users_with_bios['bio'].apply(lambda x: len(x.split()))
slope_bio_followers = linregress(users_with_bios['bio_word_count'], users_with_bios['followers']).slope.round(3)
print("Slope of followers on bio word count:", slope_bio_followers)

# 14. Users with most weekend-created repositories
# Filters for repos created on weekends and lists the top 5 users with the most weekend-created repos
repos['weekday'] = repos['created_at'].dt.weekday
weekend_repos = repos[repos['weekday'] >= 5]
weekend_repo_counts = weekend_repos['login'].value_counts().head(5).index.tolist()
print("Users with most weekend-created repos:", ', '.join(weekend_repo_counts))

# 15. Email sharing among hireable users
# Calculates the fraction of hireable and non-hireable users who have shared their email
hireable_with_email_fraction = users[users['hireable'] == True]['email'].notnull().mean()
nonhireable_with_email_fraction = users[users['hireable'] == False]['email'].notnull().mean()
email_hireable_difference = (hireable_with_email_fraction - nonhireable_with_email_fraction).round(3)
print("Difference in email sharing (hireable vs. non-hireable):", email_hireable_difference)

# 16. Most common surname
# Extracts surnames from names and identifies the most common surname(s)
users['surname'] = users['name'].fillna('').apply(lambda x: x.split()[-1] if x.strip() and len(x.split()) > 1 else None)
most_common_surname_counts = users['surname'].value_counts()
if not most_common_surname_counts.empty:
    top_surnames = most_common_surname_counts[most_common_surname_counts == most_common_surname_counts.max()].index.sort_values()
    top_surnames = ', '.join(top_surnames)
else:
    top_surnames = "No common surname found"
print("Most common surname(s):", top_surnames)
