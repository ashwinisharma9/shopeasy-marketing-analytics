# pip install pandas nltk pyodbc sqlalchemy

import pandas as pd
import pyodbc
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download VADER lexicon
nltk.download('vader_lexicon')

# Function to fetch data from SQL Server
def fetch_data_from_sql():

    # SQL Server connection string
    conn_str = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=.\\SQLEXPRESS;"
        "Database=PortfolioProject_MarketingAnalytics;"
        "Trusted_Connection=yes;"
    )

    # Connect to SQL Server
    conn = pyodbc.connect(conn_str)

    # SQL query
    query = """
    SELECT 
        ReviewID,
        CustomerID,
        ProductID,
        ReviewDate,
        Rating,
        ReviewText
    FROM dbo.customer_reviews
    """

    # Read SQL data into pandas DataFrame
    df = pd.read_sql(query, conn)

    # Close connection
    conn.close()

    return df

# Fetch data
customer_reviews_df = fetch_data_from_sql()

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Function to calculate sentiment score
def calculate_sentiment(review):

    sentiment = sia.polarity_scores(str(review))

    return sentiment['compound']

# Function to categorize sentiment
def categorize_sentiment(score, rating):

    if score > 0.05:

        if rating >= 4:
            return 'Positive'

        elif rating == 3:
            return 'Mixed Positive'

        else:
            return 'Mixed Negative'

    elif score < -0.05:

        if rating <= 2:
            return 'Negative'

        elif rating == 3:
            return 'Mixed Negative'

        else:
            return 'Mixed Positive'

    else:

        if rating >= 4:
            return 'Positive'

        elif rating <= 2:
            return 'Negative'

        else:
            return 'Neutral'

# Function to create sentiment buckets
def sentiment_bucket(score):

    if score >= 0.5:
        return '0.5 to 1.0'

    elif 0.0 <= score < 0.5:
        return '0.0 to 0.49'

    elif -0.5 <= score < 0.0:
        return '-0.49 to 0.0'

    else:
        return '-1.0 to -0.5'

# Calculate sentiment score
customer_reviews_df['SentimentScore'] = customer_reviews_df['ReviewText'].apply(calculate_sentiment)

# Categorize sentiment
customer_reviews_df['SentimentCategory'] = customer_reviews_df.apply(
    lambda row: categorize_sentiment(row['SentimentScore'], row['Rating']),
    axis=1
)

# Create sentiment buckets
customer_reviews_df['SentimentBucket'] = customer_reviews_df['SentimentScore'].apply(sentiment_bucket)

# Display first 5 rows
print(customer_reviews_df.head())

# Save output CSV
customer_reviews_df.to_csv(
    'fact_customer_reviews_with_sentiment.csv',
    index=False
)

print("Sentiment Analysis Completed Successfully!")