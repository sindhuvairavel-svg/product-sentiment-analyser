import streamlit as st
from scraper import scrape_reviews
from sentiment import analyze_sentiment
from database import create_database, save_review


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Product Sentiment Analyzer",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #eef2ff 0%, #f8fafc 50%, #ecfeff 100%);
}

/* Main container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* Main title */
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #312e81;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 17px;
    color: #64748b;
    margin-bottom: 30px;
}


/* Dashboard cards */

.card {
    padding: 22px;
    border-radius: 18px;
    min-height: 135px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    text-align: center;
    margin-bottom: 20px;
}

.total-card {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
}

.positive-card {
    background: linear-gradient(135deg, #059669, #10b981);
    color: white;
}

.neutral-card {
    background: linear-gradient(135deg, #d97706, #f59e0b);
    color: white;
}

.negative-card {
    background: linear-gradient(135deg, #dc2626, #f43f5e);
    color: white;
}

.card-icon {
    font-size: 30px;
}

.card-title {
    font-size: 16px;
    margin-top: 5px;
}

.card-value {
    font-size: 34px;
    font-weight: 800;
    margin-top: 5px;
}


/* Review cards */

.review-card {
    background: white;
    padding: 18px;
    margin: 12px 0;
    border-radius: 15px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.07);
}

.positive-review {
    border-left: 6px solid #10b981;
}

.neutral-review {
    border-left: 6px solid #f59e0b;
}

.negative-review {
    border-left: 6px solid #ef4444;
}


/* Section heading */

.section-title {
    color: #312e81;
    font-size: 25px;
    font-weight: 750;
    margin-top: 15px;
}


/* Welcome boxes */

.welcome-box {
    background: white;
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 5px 20px rgba(0,0,0,0.07);
    min-height: 180px;
}


/* Footer */

.footer {
    text-align: center;
    color: #64748b;
    margin-top: 40px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# DATABASE
# =========================================================

create_database()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">📊 Product Sentiment Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Product Review & Sentiment Analysis Dashboard'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## ⚙️ Analysis Panel")

    st.markdown("---")

    product = st.text_input(
        "🛍️ Enter Product Name",
        placeholder="Example: iPhone"
    )

    analyze_button = st.button(
        "🔍 Analyze Reviews",
        use_container_width=True
    )

    st.markdown("---")

    st.markdown("### 📌 How it works")

    st.write("1️⃣ Enter product name")
    st.write("2️⃣ Collect reviews")
    st.write("3️⃣ Analyze sentiment")
    st.write("4️⃣ Generate dashboard")

    st.markdown("---")

    st.info(
        "The system classifies reviews into "
        "Positive, Neutral and Negative sentiments."
    )


# =========================================================
# ANALYSIS
# =========================================================

if analyze_button:

    if product.strip() == "":

        st.warning("⚠️ Please enter a product name.")

    else:

        with st.spinner("🔄 Analyzing product reviews..."):

            reviews = scrape_reviews(product)

            results = []

            for review in reviews:

                sentiment, polarity = analyze_sentiment(review)

                save_review(
                    product,
                    review,
                    sentiment,
                    polarity
                )

                results.append({
                    "review": review,
                    "sentiment": sentiment,
                    "polarity": polarity
                })


        # =================================================
        # CALCULATE COUNTS
        # =================================================

        total = len(results)

        positive = sum(
            1 for item in results
            if item["sentiment"] == "Positive"
        )

        neutral = sum(
            1 for item in results
            if item["sentiment"] == "Neutral"
        )

        negative = sum(
            1 for item in results
            if item["sentiment"] == "Negative"
        )


        # =================================================
        # PRODUCT TITLE
        # =================================================

        st.markdown(
            f"""
            <div class="section-title">
                🛍️ Analysis Results: {product}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")


        # =================================================
        # DASHBOARD CARDS
        # =================================================

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.markdown(
                f"""
                <div class="card total-card">
                    <div class="card-icon">📝</div>
                    <div class="card-title">Total Reviews</div>
                    <div class="card-value">{total}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with col2:

            st.markdown(
                f"""
                <div class="card positive-card">
                    <div class="card-icon">😊</div>
                    <div class="card-title">Positive Reviews</div>
                    <div class="card-value">{positive}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with col3:

            st.markdown(
                f"""
                <div class="card neutral-card">
                    <div class="card-icon">😐</div>
                    <div class="card-title">Neutral Reviews</div>
                    <div class="card-value">{neutral}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with col4:

            st.markdown(
                f"""
                <div class="card negative-card">
                    <div class="card-icon">😞</div>
                    <div class="card-title">Negative Reviews</div>
                    <div class="card-value">{negative}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


        # =================================================
        # SENTIMENT DISTRIBUTION
        # =================================================

        st.markdown(
            '<div class="section-title">📊 Sentiment Distribution</div>',
            unsafe_allow_html=True
        )

        st.write("")


        chart_data = {
            "Positive": positive,
            "Neutral": neutral,
            "Negative": negative
        }

        st.bar_chart(chart_data)


        # =================================================
        # PERCENTAGE
        # =================================================

        if total > 0:

            positive_percent = (positive / total) * 100
            neutral_percent = (neutral / total) * 100
            negative_percent = (negative / total) * 100

        else:

            positive_percent = 0
            neutral_percent = 0
            negative_percent = 0


        st.markdown(
            '<div class="section-title">📈 Sentiment Percentage</div>',
            unsafe_allow_html=True
        )

        p1, p2, p3 = st.columns(3)


        with p1:

            st.metric(
                "😊 Positive",
                f"{positive_percent:.1f}%"
            )


        with p2:

            st.metric(
                "😐 Neutral",
                f"{neutral_percent:.1f}%"
            )


        with p3:

            st.metric(
                "😞 Negative",
                f"{negative_percent:.1f}%"
            )


        # =================================================
        # OVERALL SENTIMENT
        # =================================================

        st.markdown(
            '<div class="section-title">🎯 Overall Sentiment</div>',
            unsafe_allow_html=True
        )


        if positive > negative and positive > neutral:

            st.success(
                "😊 Overall Sentiment: POSITIVE"
            )

        elif negative > positive and negative > neutral:

            st.error(
                "😞 Overall Sentiment: NEGATIVE"
            )

        else:

            st.warning(
                "😐 Overall Sentiment: NEUTRAL"
            )


        # =================================================
        # REVIEW DETAILS
        # =================================================

        st.markdown(
            '<div class="section-title">📝 Review Details</div>',
            unsafe_allow_html=True
        )


        for index, item in enumerate(results, start=1):

            sentiment = item["sentiment"]

            if sentiment == "Positive":

                icon = "😊"
                css_class = "positive-review"

            elif sentiment == "Negative":

                icon = "😞"
                css_class = "negative-review"

            else:

                icon = "😐"
                css_class = "neutral-review"


            st.markdown(
                f"""
                <div class="review-card {css_class}">

                    <h4>
                        {icon} Review {index}
                    </h4>

                    <p>
                        {item["review"]}
                    </p>

                    <b>Sentiment:</b>
                    {sentiment}

                    &nbsp;&nbsp;&nbsp;

                    <b>Polarity:</b>
                    {item["polarity"]:.2f}

                </div>
                """,
                unsafe_allow_html=True
            )


        # =================================================
        # SUCCESS MESSAGE
        # =================================================

        st.success(
            "✅ Product review analysis completed successfully!"
        )


# =========================================================
# WELCOME PAGE
# =========================================================

else:

    st.markdown("---")

    st.markdown(
        '<div class="section-title">🚀 Welcome</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Analyze product reviews and understand customer opinions "
        "using sentiment analysis."
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            """
            <div class="welcome-box">

                <h2>🔍</h2>

                <h3>Review Analysis</h3>

                <p>
                Analyze product reviews automatically
                and extract useful information.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            """
            <div class="welcome-box">

                <h2>🤖</h2>

                <h3>AI Sentiment</h3>

                <p>
                Identify Positive, Neutral and
                Negative customer opinions.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            """
            <div class="welcome-box">

                <h2>📊</h2>

                <h3>Visual Dashboard</h3>

                <p>
                View sentiment statistics and
                review insights clearly.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        """
        <div class="footer">
            📊 Product Sentiment Analyzer | AI-Based Review Analysis
        </div>
        """,
        unsafe_allow_html=True
    )