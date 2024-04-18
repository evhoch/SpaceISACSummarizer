

from newspaper import Article, Source, Config
import newspaper


# In[38]:


keywords = [
    "Anti-Satellite (ASAT) Weapon",
    "ASAT Testing",
    "Business Email Compromise",
    "China Cyber Threat",
    "Cyber Attacks on Supply Chain",
    "Cyber Attacks on Critical Infrastructure",
    "Cyber Attacks on Satellites",
    "Cyber Hacks",
    "Cyber Intelligence",
    "Cyber Security",
    "Cyber Security Threat",
    "Cyber Threats",
    "Cyber Threat to Space Systems",
    "GPS Interference",
    "GPS Spoofing",
    "HawkEye360",
    "Iranian Cyber Threat",
    "Malware",
    "Malicious Cyber Activity",
    "North Korea Cyber Threat",
    "Russia Cyber Threat",
    "Space Supply Chain",
    "Space Intelligence",
    "Space Industry Intelligence",
    "Space ISAC",
    "Space Launch",
    "Supply Chain",
    "Supply Chain Attack",
    "Supply Chain Management",
    "Advanced Persistent Threats in cyber",
    "Brute force password attack",
    "China Cyber attack",
    "CISA",
    "Credential Harvesting",
    "Cyber Companies",
    "Cyber Operations",
    "Cyber Supply Chain",
    "Cyber Vulnerabilites",
    "Cybersecurity",
    "Global Cybercrime",
    "GPS Interference / Jamming",
    "Hackers",
    "Hackers and Space",
    "Hacking Threats",
    "GPS jamming",
    "Malicious Cyber Attack",
    "phishing",
    "Ransomware",
    "Orbital Debris",
    "Remote Access Trojans",
    "Positioning, Navigation, and Tracking",
    "Satellite",
    "Satellite hack",
    "Satellite spoofing",
    "Satellite threats and targets",
    "Space Debris",
    "Space manufacturing",
    "Space launch",
    "Space Sanctions",
    "Space Sector development",
    "Space related critical infrastructure",
    "Space System Operations",
    "Space Vulnerability",
    "spear phishing",
    "Zero-day exploitation"
]


from newspaper import Article, Config
import newspaper


def scrape_news_site(url, user_agent, max_articles=None):
    # Create a configuration object
    config = Config()
    # Set the provided custom user agent
    config.browser_user_agent = user_agent
    
    # Build a Source object to represent the site with the specified configuration
    paper = newspaper.build(url, config=config, memoize_articles=False, language='en')
    
    # List to hold all articles' information
    articles_info = []
    article_count = 0

    # Iterate through the articles found on the homepage and extract details
    for article in paper.articles:
        if max_articles is not None and article_count >= max_articles:
            break  # Stop the loop if we've reached the max number of articles
        
        # Set the same config for the article
        article.config = config
        
        # Download the article's content
        article.download()
        
        # Parse the downloaded content
        try:
            article.parse()
        except Exception as e:
            print(f"Failed to parse {article.url}: {e}")
            continue  # If parsing fails, skip to the next article

        # Store the article's information
        article_info = {
            'title': article.title,
            'url': article.url,
            'text': article.text
        }
        articles_info.append(article_info)
        article_count += 1

        # Print the title, URL, and the beginning of the article text
        print(f"Title: {article.title}")
        print(f"URL: {article.url}")
        print(f"Text: {article.text[:200]}...")  # Print the first 200 characters of the text
        print('----------------------------------')

    return articles_info




# In[40]:


custom_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
news_url = 'https://www.axios.com'

# Scrape the given news site
#scraped_articles = scrape_news_site(news_url, custom_user_agent)



# In[41]:


#len(scraped_articles)


# In[42]:


import nltk
nltk.download('stopwords')


# In[52]:


from fuzzywuzzy import process
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def tokenize_keywords(keywords):
    # Split each keyword phrase into a set of individual tokens
    tokens = set()
    for keyword in keywords:
        # Tokenize the keyword and remove stop words
        words = keyword.lower().split()
        meaningful_words = [word for word in words if word not in stop_words]
        tokens.update(meaningful_words)
    return tokens


def filter_articles_by_title(articles, keywords, threshold=90):
    # Tokenize the keywords for better matching
    keyword_tokens = tokenize_keywords(keywords)

    # Define a minimum match score for fuzzy matching
    min_match_score = threshold  # You can adjust this threshold

    # Create a list to hold articles that match the keywords
    filtered_articles = []

    # Iterate through the articles
    for article in articles:
        # Tokenize the title of each article
        title_tokens = set(article['title'].lower().split())

        # Perform fuzzy matching
        for token in title_tokens:
            match, score = process.extractOne(token, keyword_tokens)
            if score >= min_match_score:
                filtered_articles.append(article)
                break  # Break to avoid adding the same article multiple times
    
    return filtered_articles

