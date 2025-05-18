import streamlit as st
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import plotly.graph_objects as go



# Set up the page layout
st.set_page_config(
    page_title="State and Lake Chicago Tavern Reviews",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load the reviews data from the JSON file
with open('claude_response.json', 'r') as file:
    reviews = json.load(file)

# Custom CSS for the entire app
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to bottom, #EA2727FF, #1a2a6c, #76142CFF);
        color: #ecf0f1;
        font-family: 'Garamond', serif;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(to bottom, #1a2a6c, #b21f1f, #fdbb2d);
        color: white;
        font-family: 'Garamond', serif;
    }
    .sidebar .sidebar-content h1, .sidebar .sidebar-content h2, .sidebar .sidebar-content h3, .sidebar .sidebar-content h4, .sidebar .sidebar-content h5, .sidebar .sidebar-content h6 {
        color: white;
    }
    .sidebar .sidebar-content .stRadio > label {
        color: white;
    }
    .sidebar .sidebar-content .stRadio > div > div {
        background-color: #e74c3c;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        transition: background-color 0.3s ease;
    }
    .sidebar .sidebar-content .stRadio > div > div:hover {
        background-color: #c0392b;
    }
    .sidebar .sidebar-content .stRadio > div > div:checked {
        background-color: #e74c3c;
        color: white;
    }
    .stButton>button {
        background-color: #e74c3c;
        color: white;
        padding: 12px 28px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-family: 'Garamond', serif;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #ffffff;
    }
    .heading {
        font-size: 3em;
        color: #e74c3c;
        font-family: 'Garamond', serif;
        font-weight: bold;
        text-shadow: 3px 3px 8px rgba(0, 0, 0, 0.2);
        text-align: center;
    }
    .features-list {
        font-family: 'Garamond', serif;
        font-size: 1.3em;
        padding: 0;
    }
    .feature-item {
        display: block;
        margin: 10px 0;
        color: #ecf0f1;
    }
    .highlight {
        color: #2ecc71;
    }
    .highlight-blue {
        color: #3498db;
    }
    .btn-container {
        margin-top: 40px;
        text-align: center;
    }
    .review-card {
        background-color: #2c3e50;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .review-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
    }
    .review-heading {
        font-size: 1.6em;
        color: #f39c12;
        font-weight: bold;
        margin-bottom: 15px;
        text-align: center;
    }
    .review-content {
        font-size: 1.2em;
        color: white;
        margin-bottom: 10px;
    }
    .review-highlight-food {
        color: limegreen;
        font-weight: bold;
    }
    .review-highlight-service {
        color: cyan;
        font-weight: bold;
    }
    .rating-stars {
        color: #f1c40f;
        font-size: 1.3em;
        margin-top: 5px;
        text-align: center;
    }
    .key {
        font-weight: bold;
        color: #f39c12;
    }
    .value {
        color: #bdc3c7;
    }
    .no-data {
        color: #95a5a6;
        font-style: italic;
    }
    footer {
        text-align: center;
        margin-top: 50px;
        color: #bdc3c7;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("Choose an option to explore:")

# Sidebar options
options = ["Splash Screen", "Dashboard", "Data Table", "Comparison Charts","Overall Summary"]
# selection = st.sidebar.radio("Go to", options)
if 'selection' not in st.session_state:
    st.session_state.selection = "Splash Screen"
selection = st.sidebar.radio("Go to", options, index=options.index(st.session_state.selection))

# Splash Screen Section
if selection == "Splash Screen":
    def splash_screen():
        st.markdown(
            """
            <h1 class="heading">Welcome to State and Lake Chicago Tavern Reviews 👋</h1>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="features-list">
                <span class="feature-item">🔍 <strong>Search and filter reviews</strong></span>
                <span class="feature-item">🔆 Highlighted text for <span class="highlight">food quality</span> and <span class="highlight-blue">staff service</span></span>
                <span class="feature-item">🧭 <strong>Easy navigation</strong></span>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button('Go to Dashboard'):
            global selection
            st.session_state.selection = "Dashboard"
            st.rerun()
            selection = "Dashboard"
    splash_screen()

elif selection == "Dashboard":
    def highlight_text(text, color):
        """Returns text styled with the specified color."""
        return f"<span style='color:{color}; font-weight:bold'>{text}</span>"

    def extract_numeric_rating(rating_str):
        import re
        match = re.search(r'\d+', str(rating_str))
        return int(match.group()) if match else 0

    def format_nested_data(data):
        """Recursively formats nested data into HTML-friendly content."""
        if isinstance(data, dict):
            return "<ul>" + "".join(f"<li><b style='color: #f39c12;'>{key.capitalize()}</b>: {format_nested_data(value)}</li>" for key, value in data.items()) + "</ul>"
        elif isinstance(data, list):
            return "<ul>" + "".join(f"<li>{format_nested_data(item)}</li>" for item in data) + "</ul>"
        else:
            return str(data)

    def dashboard(reviews):
        st.markdown("<h1 style='color: #ecf0f1; text-align:center; padding: 20px;'>State and Lake Restaurant Reviews</h1>", unsafe_allow_html=True)

        search_query = st.text_input(
            'Search for reviews',
            placeholder='Enter keywords to search reviews...',
            help='Type keywords to filter reviews',
        )

        filtered_reviews = [
            review for review in reviews
            if search_query.lower() in json.dumps(review).lower()
        ] if search_query else reviews

        if not filtered_reviews:
            st.warning("No reviews match your search criteria.")
        else:
            st.markdown(f"<p style='color: #ecf0f1;'>Displaying {len(filtered_reviews)} result(s) for query: <i>{search_query}</i></p>", unsafe_allow_html=True)

        for review in filtered_reviews:
            st.markdown("<hr>", unsafe_allow_html=True)
            # st.markdown("<hr>", unsafe_allow_html=True)
            with st.container():
                # Semi-transparent background to contrast with gradient
                # st.markdown(
                #     """
                #     <div style='background-color: rgba(0, 0, 0, 0.5); padding: 20px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);'>
                #     """,
                #     unsafe_allow_html=True
                # )
                review_name = review.get('name', 'Anonymous')
                dining_time = review.get('dining_time', 'Unknown Date')
                rating = extract_numeric_rating(review.get('rating', 0))

                # Styling the name and dining time with white text for contrast
                st.markdown(f"<h3 style='color: #2ecc71; text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.6);text-align:center;'>{review_name}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #A3F5B2FF; text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.6);text-align:center;'>{dining_time}</p>", unsafe_allow_html=True)

                # Star rating with a gold color for better contrast on gradient
                stars = "★" * rating + "☆" * (5 - rating)
                st.markdown(f"<p style='font-size:20px; color:#f39c12; text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.6);text-align:center;'>{stars}</p>", unsafe_allow_html=True)

                # Food quality section
                food_quality = review.get('food_quality', 'No food quality provided')
                st.markdown("<h4 style='color:#e74c3c; padding: 5px; text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.6);'>Food Quality</h4>", unsafe_allow_html=True)
                st.markdown(format_nested_data(food_quality), unsafe_allow_html=True)

                # Staff service section
                staff_service = review.get('staff_service', 'No staff service provided')
                st.markdown("<h4 style='color:#3498db; padding: 5px; text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.6);'>Staff Service</h4>", unsafe_allow_html=True)
                st.markdown(format_nested_data(staff_service), unsafe_allow_html=True)

                # Other comments section
                other_comments = review.get('comments', [])
                if other_comments:
                    st.markdown("<h4 style='color:#9b59b6; text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.6);'>Other Comments</h4>", unsafe_allow_html=True)
                    st.markdown(format_nested_data(other_comments), unsafe_allow_html=True)
                # else:
                #     st.markdown("<p style='color:#7f8c8d; text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.6);'>No additional comments available.</p>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<footer style='text-align:center; padding: 10px;'>Powered by <b>Streamlit</b> | Designed by Hamda Shahid</footer>", unsafe_allow_html=True)

    dashboard(reviews)

# Data Table Section
elif selection == "Data Table":
    st.header("📊 Explore Data Table")

    # Load the data from the CSV files
    csv_file1 = 'state_and_lake_chicago_tavern_reviews.csv'
    csv_file2 = 'second_restaurant_reviews.csv'
    df1 = pd.read_csv(csv_file1)
    df2 = pd.read_csv(csv_file2)

    # Display the first data table
    st.subheader("State and Lake Chicago Tavern Reviews")
    st.dataframe(df1)
    st.download_button(
        label="📥 Download State and Lake Data as CSV",
        data=df1.to_csv(index=False),
        file_name="state_and_lake_chicago_tavern_reviews.csv",
        mime="text/csv",
    )

    # Display the second data table
    st.subheader("Heirloom - New Haven Reviews")
    st.dataframe(df2)
    st.download_button(
        label="📥 Download Second Restaurant Data as CSV",
        data=df2.to_csv(index=False),
        file_name="second_restaurant_reviews.csv",
        mime="text/csv",
    )

# # Charts Section
# # Charts Section
# Comparison Charts Section
elif selection == "Comparison Charts":

    # Function to convert 'Date of Review' to datetime
    def convert_date(date_str):
        if 'days ago' in date_str:
            days_ago = int(date_str.split()[1])
            return datetime.now() - timedelta(days=days_ago)
        elif 'Dined on' in date_str:
            return pd.to_datetime(date_str.replace('Dined on ', ''), format='%B %d, %Y')
        else:
            return pd.to_datetime(date_str, format="%Y-%m-%d")

    # Load dataframes from CSV files
    df = pd.read_csv('state_and_lake_chicago_tavern_reviews.csv')
    df2 = pd.read_csv('second_restaurant_reviews.csv')

    # Convert 'Date of Review' to datetime format
    review_dates_1 = df["Date of Review"].apply(convert_date)
    review_dates_2 = df2["Date of Review"].apply(convert_date)

    # Convert 'Rating' to numeric values
    ratings_1 = df["Rating"].apply(lambda x: int(x.split()[0]))
    ratings_2 = df2["Rating"].apply(lambda x: int(x.split()[0]))

    # Create new DataFrames with converted dates and ratings
    df1_resampled = pd.DataFrame({'Date': review_dates_1, 'Rating': ratings_1})
    df2_resampled = pd.DataFrame({'Date': review_dates_2, 'Rating': ratings_2})

    # Resample data to yearly frequency and calculate the mean rating for each year
    df1_yearly = df1_resampled.resample('YE', on='Date').mean()
    df2_yearly = df2_resampled.resample('YE', on='Date').mean()

    # Define custom year ranges and dynamic filters
    st.sidebar.header("Filter Data")
    min_year, max_year = st.sidebar.slider(
        "Select Year Range:", 
        min_value=int(df1_yearly.index.year.min()),
        max_value=int(df2_yearly.index.year.max()),
        value=(2010, 2024),
        step=1
    )

    # Filter data based on user-selected year range
    df1_yearly = df1_yearly[(df1_yearly.index.year >= min_year) & (df1_yearly.index.year <= max_year)]
    df2_yearly = df2_yearly[(df2_yearly.index.year >= min_year) & (df2_yearly.index.year <= max_year)]

    # Plot for Restaurant 1
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df1_yearly.index,
        y=df1_yearly['Rating'],
        mode='lines+markers',
        name='Restaurant 1',
        line=dict(shape='linear', width=2, color='#636EFA'),
        marker=dict(size=8, color='#636EFA')
    ))
    fig1.update_layout(
        title='Rating Trends for State and Lake Chicago Tavern',
        xaxis_title='Year',
        yaxis_title='Average Rating',
        xaxis=dict(showgrid=True, tickangle=45),
        yaxis=dict(showgrid=True),
        template='plotly_white',
        font=dict(size=14),
        plot_bgcolor='#F9F9F9',
        title_font=dict(size=18)
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Plot for Restaurant 2
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df2_yearly.index,
        y=df2_yearly['Rating'],
        mode='lines+markers',
        name='Restaurant 2',
        line=dict(shape='linear', dash='dash', width=2, color='#EF553B'),
        marker=dict(size=8, symbol='x', color='#EF553B')
    ))
    fig2.update_layout(
        title='Rating Trends for Heirloom - New Haven',
        xaxis_title='Year',
        yaxis_title='Average Rating',
        xaxis=dict(showgrid=True, tickangle=45),
        yaxis=dict(showgrid=True),
        template='plotly_white',
        font=dict(size=14),
        plot_bgcolor='#F9F9F9',
        title_font=dict(size=18)
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Comparison Plot
    fig = go.Figure()

    # Add traces for both restaurants
    fig.add_trace(go.Scatter(
        x=df1_yearly.index,
        y=df1_yearly['Rating'],
        mode='lines+markers',
        name='State and Lake Chicago Tavern',
        line=dict(shape='linear', width=2, color='#636EFA'),
        marker=dict(size=8, color='#636EFA')
    ))

    fig.add_trace(go.Scatter(
        x=df2_yearly.index,
        y=df2_yearly['Rating'],
        mode='lines+markers',
        name='Heirloom - New Haven',
        line=dict(shape='linear', dash='dash', width=2, color='#EF553B'),
        marker=dict(size=8, symbol='x', color='#EF553B')
    ))

    # Highlight peak ratings with annotations
    max_rating_1 = df1_yearly['Rating'].max()
    max_rating_2 = df2_yearly['Rating'].max()
    peak_year_1 = df1_yearly['Rating'].idxmax()
    peak_year_2 = df2_yearly['Rating'].idxmax()

    fig.add_annotation(
        x=peak_year_1, 
        y=max_rating_1,
        text=f"Peak: {max_rating_1:.1f}",
        showarrow=True,
        arrowhead=1,
        # bgcolor="yellow"
        # color="black"
        # arrowcolor="black"
        arrowcolor="black",
        bgcolor="blue",
        font=dict(color="white")
    )

    fig.add_annotation(
        x=peak_year_2, 
        y=max_rating_2,
        text=f"Peak: {max_rating_2:.1f}",
        showarrow=True,
        arrowhead=1,
        arrowcolor="black",
        bgcolor="red",
        font=dict(color="white")
    )

    # Update layout for better visual appeal
    fig.update_layout(
        title='Rating Comparison Trends for State and Lake Restaurant and Heirloom - New Haven Restaurant',
        xaxis_title='Year',
        yaxis_title='Average Rating',
        xaxis=dict(showgrid=True, tickangle=45),
        yaxis=dict(showgrid=True),
        legend_title='Restaurant',
        template='plotly_white',
        font=dict(size=14),
        plot_bgcolor='#F9F9F9',
        title_font=dict(size=18),
        hovermode='x unified'
    )

    # Display the comparison plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

elif selection == "Overall Summary":
    # Overall Summary Section
    st.header("📋 Overall Review Summary")
    
    # Load Data
    df = pd.read_csv('state_and_lake_chicago_tavern_reviews.csv')
    df2 = pd.read_csv('second_restaurant_reviews.csv')
    
    # Function to compute review summary
    def overall_review_summary(df, restaurant_name):
        avg_rating = df['Rating'].apply(lambda x: int(x.split()[0])).mean()
        total_reviews = len(df)
        positive_reviews = df[df['Rating'].str.contains('5 stars')].shape[0]
        negative_reviews = df[df['Rating'].str.contains('1 star')].shape[0]
        
        return {
            "restaurant_name": restaurant_name,
            "avg_rating": avg_rating,
            "total_reviews": total_reviews,
            "positive_reviews": positive_reviews,
            "negative_reviews": negative_reviews
        }

    # Summarize reviews for both restaurants
    summary1 = overall_review_summary(df, "State and Lake Chicago Tavern")
    summary2 = overall_review_summary(df2, "Heirloom - New Haven")

    # Define a helper function to display styled metrics
    def display_summary(summary):
        st.subheader(f"🍴 {summary['restaurant_name']}")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🌟 Average Rating", f"{summary['avg_rating']:.2f} stars")
        with col2:
            st.metric("📝 Total Reviews", summary["total_reviews"])
        with col3:
            st.metric("😊 Positive Reviews", summary["positive_reviews"])
        
        col4, col5 = st.columns(2)
        with col4:
            st.metric("☹️ Negative Reviews", summary["negative_reviews"])
        with col5:
            pos_percentage = (summary["positive_reviews"] / summary["total_reviews"]) * 100
            st.metric("📊 Positive Review %", f"{pos_percentage:.1f}%")

    # Display summaries with an attractive layout
    st.markdown("### 🏆 Review Summaries")
    with st.container():
        st.write("---")  # Separator for better layout
        display_summary(summary1)
        st.write(" ")
        st.write(" ")
        st.write(" ")
        display_summary(summary2)
    
    # Add an interactive component (e.g., download button)
    st.download_button(
        label="📥 Download Summary",
        data=f"Summary for State and Lake Chicago Tavern:\n{summary1}\n\nSummary for Heirloom - New Haven:\n{summary2}",
        file_name="overall_review_summary.txt",
        mime="text/plain"
    )
    