# 📊 Toronto GitHub Users Data Analysis

### 🔍 Key Insights

1. **Data Collection**: I used the GitHub API to gather profiles of Toronto-based users with over 100 followers. The script pulls data in batches, navigating through pages of results and respecting API rate limits by pausing and retrying when needed. For each user, I collected detailed profile info and up to 500 of their most recent repositories, capturing details like programming language, license, and project stats. Finally, all the data is organized into CSV files for straightforward analysis.

2. **Interesting Fact**: Surprisingly, many top-followed Toronto developers focus on niche or emerging languages over popular ones like JavaScript or Python. This trend shows that unique expertise in less common tech can attract substantial follower engagement, possibly because it demonstrates specialized skills that are in demand but underrepresented.

3. **Developer Recommendation**: Developers in Toronto aiming to boost their visibility should explore contributions in data science and open-source projects, as these areas attract high engagement. Active involvement in popular fields like machine learning not only connects with a larger community but also aligns with local trends, making it easier to build a strong follower base.

---

## 📖 Project Overview

This project uses GitHub's API to analyze Toronto-based users with significant follower counts, focusing on their profiles, repositories, and language choices. The data collection script (`analysis.py`) and the analysis script (`analysisResults.py`) work together to provide structured output in two CSV files, `users.csv` and `repositories.csv`, which serve as a foundation for examining trends and insights on GitHub user influence.

### ⚙️ Process and Key Steps

1. **Data Retrieval (`analysis.py`)**: This script fetches user and repository data from the GitHub API, with rate limit handling, retry logic, and data cleaning to standardize fields.
2. **Data Cleaning**: Company names were standardized, null values were addressed, and various fields were formatted for consistency.
3. **Repository Analysis (`analysis.py`)**: For each user, up to 500 recent repositories were analyzed, focusing on language, license type, and usage of features like projects and wikis.
4. **Data Analysis (`analysisResults.py`)**: This script processes the generated CSV files, running calculations for insights like most popular languages, top users by followers, correlation analyses, and more.
5. **Output and Results**: CSV files `users.csv` and `repositories.csv` contain user and repository details, supporting further data exploration and insights.

### 🔧 Technical Overview

- **Rate Limit Management**: A built-in check in `analysis.py` ensures the script pauses when near the GitHub API rate limit, enabling seamless data gathering.
- **Error Handling**: Connection retries and exponential backoff make `analysis.py` robust against network issues.
- **Data Structuring**: `users.csv` and `repositories.csv` are designed for compatibility with popular data analysis tools, making data easy to query and interpret.

---


## 📂 Files Generated

- **`users.csv`**: Contains GitHub users' profile details, including login, name, company, email, bio, number of repositories, followers, and more.
- **`repositories.csv`**: Details each user’s repositories, including repository name, creation date, star count, primary language, and license type.

