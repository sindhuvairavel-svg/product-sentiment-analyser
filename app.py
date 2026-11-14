import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from textblob import TextBlob

# Page Config
st.set_page_config(
    page_title="Product Sentiment Analyser", page_icon="📊", layout="wide"
)

# Custom Styling (Black & Gold Theme)
st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
        color: #f0f2f6;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: #1a1c23;
        color: #ffd700;
        border: 1px solid #ffd700;
    }
    .stButton button {
        background-color: #ffd700;
        color: #0e1117;
        font-weight: bold;
        border-radius: 5px;
    }
    .stButton button:hover {
        background-color: #ffcc00;
        color: #000000;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("✨ 3D Product Sentiment Analyser Dashboard")
st.markdown(
    "Analyze product reviews interactively with 3D charts, metrics, and deep insights."
)

# 3-Column Layout for Controls / Inputs
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.subheader("📝 Input Section")
    product_name = st.text_input("Product Name", "Smart Headphones")
    review_input = st.text_area(
        "Enter Reviews (One per line)",
        "Amazing sound quality and great battery life!\nTerrible build quality, broke in two days.\nAverage product, nothing special.\nSuper comfortable and very stylish.\nWorst customer service ever experienced.",
    )

with col2:
    st.subheader("⚙️ Settings & Filters")
    sentiment_filter = st.selectbox(
        "Filter Sentiment View", ["All", "Positive", "Negative", "Neutral"]
    )
    show_3d = st.checkbox("Enable 3D Visual Effects", value=True)

with col3:
    st.subheader("💡 Quick Stats")
    reviews_list = [r.strip() for r in review_input.split("\n") if r.strip()]
    total_reviews = len(reviews_list)
    st.metric(label="Total Reviews Analyzed", value=total_reviews)

if reviews_list:
    # Process sentiments
    data = []
    for i, review in enumerate(reviews_list):
        analysis = TextBlob(review)
        polarity = analysis.sentiment.polarity
        if polarity > 0.1:
            sentiment = "Positive"
        elif polarity < -0.1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        data.append(
            {
                "ID": i + 1,
                "Review": review,
                "Polarity": polarity,
                "Subjectivity": analysis.sentiment.subjectivity,
                "Sentiment": sentiment,
            }
        )

    # Filter data based on selection
    if sentiment_filter != "All":
        filtered_data = [d for d in data if d["Sentiment"] == sentiment_filter]
    else:
        filtered_data = data

    st.markdown("---")

    # Metrics Row
    pos_count = sum(1 for d in data if d["Sentiment"] == "Positive")
    neg_count = sum(1 for d in data if d["Sentiment"] == "Negative")
    neu_count = sum(1 for d in data if d["Sentiment"] == "Neutral")

    m1, m2, m3 = st.columns(3)
    m1.metric("🟢 Positive Reviews", pos_count)
    m2.metric("🔴 Negative Reviews", neg_count)
    m3.metric("⚪ Neutral Reviews", neu_count)

    st.markdown("---")

    # Section for 3D and Advanced Charts
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("🌐 3D Sentiment Scatter Plot")
        if show_3d and data:
            # 3D Scatter Plot using Plotly (X: Review ID, Y: Polarity, Z: Subjectivity)
            fig_3d = px.scatter_3d(
                data,
                x="ID",
                y="Polarity",
                z="Subjectivity",
                color="Sentiment",
                text="Review",
                color_discrete_map={
                    "Positive": "#00CC96",
                    "Negative": "#EF553B",
                    "Neutral": "#FFA15A",
                },
                title="3D Review Space (Polarity vs Subjectivity)",
            )
            fig_3d.update_layout(
                scene=dict(
                    xaxis_title="Review ID",
                    yaxis_title="Polarity (-1 to 1)",
                    zaxis_title="Subjectivity (0 to 1)",
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f0f2f6"),
            )
            st.plotly_chart(fig_3d, use_container_width=True)
        else:
            st.info("Enable 3D view to see the 3D scatter plot.")

    with chart_col2:
        st.subheader("📊 Sentiment Distribution & Gauge")
        # Sentiment distribution bar chart
        sentiment_counts = {
            "Positive": pos_count,
            "Negative": neg_count,
            "Neutral": neu_count,
        }
        fig_bar = px.bar(
            x=list(sentiment_counts.keys()),
            y=list(sentiment_counts.values()),
            color=list(sentiment_counts.keys()),
            color_discrete_map={
                "Positive": "#00CC96",
                "Negative": "#EF553B",
                "Neutral": "#FFA15A",
            },
            labels={"x": "Sentiment", "y": "Count"},
            title="Overall Sentiment Breakdown",
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f0f2f6"),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # Additional Advanced Insights Section
    st.subheader("📈 Trend & Customer Insights Summary")
    ic1, ic2 = st.columns(2)

    with ic1:
        st.markdown("### 🏆 Key Highlights")
        if pos_count >= neg_count:
            st.success(
                "The product leans largely **Positive**, indicating good customer satisfaction."
            )
        else:
            st.warning(
                "The product has notable **Negative** feedback that requires attention."
            )

    with ic2:
        st.markdown("### 📋 Filtered Reviews Table")
        st.dataframe(filtered_data, use_container_width=True)

else:
    st.warning("Please enter some reviews to analyze.")
