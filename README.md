# Restaurant Review Analyzer

## Overview
An AI-powered dashboard for scraping, analyzing, and visualizing restaurant reviews from OpenTable. This tool helps restaurant owners and managers gain insights into customer experiences by separating food quality feedback from service-related comments.

## Features
- **Web Scraping**: Extract reviews from OpenTable using BeautifulSoup and Selenium
- **AI-Powered Analysis**: Utilize Claude AI to categorize comments into food quality vs. staff service
- **Interactive Dashboard**: Built with Streamlit for easy exploration of reviews
- **Comparative Analysis**: Compare restaurant ratings with competitors
- **Sentiment Filtering**: Separate positive and negative feedback about food and service
- **Time-Series Visualization**: Track changes in ratings over time

## Components
- `semester_project.ipynb`: Web scraping module that extracts reviews from OpenTable
- `dashboard.py`: Streamlit dashboard for visualizing and analyzing review data
- `state_and_lake_chicago_tavern_reviews.csv`: Primary restaurant review dataset
- `second_restaurant_reviews.csv`: Competitor restaurant review dataset
- `claude_response.json`: AI-processed review data with sentiment analysis

## Requirements
- Python 3.x
- Streamlit
- Pandas
- Matplotlib
- Plotly
- Selenium
- BeautifulSoup4
- Requests

## Usage
1. **Run the dashboard**:
   ```
   streamlit run dashboard.py
   ```

2. **Web scraping** (if you want to collect new reviews):
   - Open `semester_project.ipynb` in Jupyter Notebook
   - Update the URL to target a specific restaurant on OpenTable
   - Run the notebook to extract reviews

## Dashboard Sections
- **Splash Screen**: Welcome page with feature highlights
- **Dashboard**: Interactive review explorer with search functionality
- **Data Table**: Tabular view of all review data
- **Comparison Charts**: Visual comparisons between restaurants
- **Overall Summary**: Key metrics and insights

## Example
The current implementation analyzes reviews from "State and Lake Chicago Tavern" and compares them with another restaurant, visualizing differences in food quality, service ratings, and overall customer satisfaction.
