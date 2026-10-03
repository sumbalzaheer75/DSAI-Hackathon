import streamlit as st
import pandas as pd
import sqlite3
import joblib
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ShopSphere Analytics",
    page_icon="🛍️",
    layout="wide"
)


# ============================================================
# PATHS - LOCAL + STREAMLIT CLOUD
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

CHURN_MODEL_PATH = BASE_DIR / "churn_model.pkl"
SENTIMENT_MODEL_PATH = BASE_DIR / "sentiment_model.pkl"
DATABASE_PATH = BASE_DIR / "ecommerce_hackathon.db"


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #faf8ff;
}

h1, h2, h3 {
    color: #4c1d95 !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2e1065, #581c87);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #e9d5ff;
    border-top: 5px solid #7c3aed;
    padding: 18px;
    border-radius: 15px;
}

[data-testid="stMetricLabel"] {
    color: #475569 !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #4c1d95 !important;
    font-weight: 800;
}

.stButton > button {
    background-color: #7c3aed;
    color: white !important;
    border: none;
    border-radius: 10px;
    padding: 10px 25px;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #6d28d9;
    color: white !important;
}

[data-testid="stAlert"] p {
    color: #1f2937 !important;
    font-weight: 500;
}

input, textarea {
    color: #111827 !important;
}

.footer {
    text-align: center;
    color: #64748b;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD MODELS
# ============================================================

@st.cache_resource
def load_models():

    churn_model = joblib.load(
        CHURN_MODEL_PATH
    )

    sentiment_model = joblib.load(
        SENTIMENT_MODEL_PATH
    )

    return churn_model, sentiment_model


try:

    churn_model, sentiment_model = load_models()

except Exception as e:

    st.error(
        f"Model loading error: {e}"
    )

    st.stop()


# ============================================================
# DATABASE
# ============================================================

@st.cache_resource
def connect_database():

    return sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )


try:

    conn = connect_database()

except Exception as e:

    st.error(
        f"Database connection error: {e}"
    )

    st.stop()


# ============================================================
# MEMBERSHIP TYPES
# ============================================================

try:

    membership_df = pd.read_sql_query(
        """
        SELECT DISTINCT membership_type
        FROM customers
        WHERE membership_type IS NOT NULL
        ORDER BY membership_type
        """,
        conn
    )

    membership_options = (
        membership_df["membership_type"]
        .astype(str)
        .str.strip()
        .drop_duplicates()
        .tolist()
    )

except:

    membership_options = [
        "Basic",
        "Silver",
        "Gold",
        "Premium"
    ]


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "🛍️ ShopSphere"
)

st.sidebar.write(
    "E-Commerce Customer Intelligence"
)

st.sidebar.divider()


page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard",
        "👥 Churn Prediction",
        "💬 Sentiment Analysis"
    ]
)


st.sidebar.divider()

st.sidebar.write(
    "🎓 Data Science Final Hackathon"
)

st.sidebar.write(
    "👩‍💻 Sumbal Zaheer"
)


# ============================================================
# HEADER
# ============================================================

st.title(
    "🛍️ ShopSphere Analytics"
)

st.write(
    "### E-Commerce Customer Intelligence System"
)

st.caption(
    "Business Analytics • Customer Churn • Review Sentiment"
)

st.divider()


# ============================================================
# DASHBOARD
# ============================================================

if page == "📊 Dashboard":

    st.header(
        "📊 Business Dashboard"
    )

    st.write(
        "Monitor revenue, orders, customers "
        "and product performance."
    )


    # --------------------------------------------------------
    # KPI SQL
    # --------------------------------------------------------

    revenue_query = """
    SELECT
        SUM(
            quantity * unit_price * (1 - discount)
        ) AS net_revenue
    FROM orders
    WHERE quantity > 0
      AND unit_price > 0
      AND date(order_date) IS NOT NULL
    """


    orders_query = """
    SELECT
        COUNT(*) AS total_orders
    FROM orders
    WHERE quantity > 0
      AND unit_price > 0
      AND date(order_date) IS NOT NULL
    """


    customers_query = """
    SELECT
        COUNT(*) AS total_customers
    FROM customers
    """


    products_query = """
    SELECT
        COUNT(*) AS total_products
    FROM products
    """


    net_revenue = pd.read_sql_query(
        revenue_query,
        conn
    ).iloc[0]["net_revenue"]


    total_orders = pd.read_sql_query(
        orders_query,
        conn
    ).iloc[0]["total_orders"]


    total_customers = pd.read_sql_query(
        customers_query,
        conn
    ).iloc[0]["total_customers"]


    total_products = pd.read_sql_query(
        products_query,
        conn
    ).iloc[0]["total_products"]


    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    st.subheader(
        "📌 Business Overview"
    )


    c1, c2, c3, c4 = st.columns(4)


    c1.metric(
        "💰 Net Revenue",
        f"{net_revenue / 1_000_000:.1f}M"
    )


    c2.metric(
        "📦 Valid Orders",
        f"{total_orders:,}"
    )


    c3.metric(
        "👥 Customers",
        f"{total_customers:,}"
    )


    c4.metric(
        "🛒 Products",
        f"{total_products:,}"
    )


    st.write("")


    # --------------------------------------------------------
    # MONTHLY REVENUE
    # --------------------------------------------------------

    monthly_query = """
    SELECT

        strftime(
            '%Y-%m',
            order_date
        ) AS month,

        SUM(
            quantity *
            unit_price *
            (1 - discount)
        ) AS net_revenue

    FROM orders

    WHERE quantity > 0
      AND unit_price > 0
      AND date(order_date) IS NOT NULL

    GROUP BY month

    ORDER BY month
    """


    monthly_revenue = pd.read_sql_query(
        monthly_query,
        conn
    )


    # --------------------------------------------------------
    # CATEGORY REVENUE
    # --------------------------------------------------------

    category_query = """
    SELECT

        LOWER(
            TRIM(p.category)
        ) AS category,

        SUM(
            o.quantity *
            o.unit_price *
            (1 - o.discount)
        ) AS net_revenue

    FROM orders o

    JOIN products p
        ON o.product_id = p.product_id

    WHERE o.quantity > 0
      AND o.unit_price > 0
      AND date(o.order_date) IS NOT NULL

    GROUP BY
        LOWER(TRIM(p.category))

    ORDER BY
        net_revenue DESC
    """


    category_revenue = pd.read_sql_query(
        category_query,
        conn
    )


    category_revenue["category"] = (
        category_revenue["category"]
        .str.title()
    )


    # --------------------------------------------------------
    # CITY REVENUE
    # --------------------------------------------------------

    city_query = """
    SELECT

        LOWER(
            TRIM(c.city)
        ) AS city,

        SUM(
            o.quantity *
            o.unit_price *
            (1 - o.discount)
        ) AS net_revenue

    FROM orders o

    JOIN customers c
        ON o.customer_id = c.customer_id

    WHERE o.quantity > 0
      AND o.unit_price > 0
      AND date(o.order_date) IS NOT NULL

    GROUP BY
        LOWER(TRIM(c.city))

    ORDER BY
        net_revenue DESC
    """


    city_revenue = pd.read_sql_query(
        city_query,
        conn
    )


    city_revenue["city"] = (
        city_revenue["city"]
        .str.title()
    )


    # --------------------------------------------------------
    # RETURN RATE
    # --------------------------------------------------------

    return_query = """
    SELECT

        LOWER(
            TRIM(p.category)
        ) AS category,

        AVG(
            CASE
                WHEN o.returned = 1
                THEN 1.0
                ELSE 0.0
            END
        ) * 100 AS return_rate

    FROM orders o

    JOIN products p
        ON o.product_id = p.product_id

    WHERE o.quantity > 0
      AND o.unit_price > 0
      AND date(o.order_date) IS NOT NULL

    GROUP BY
        LOWER(TRIM(p.category))

    ORDER BY
        return_rate DESC
    """


    return_rate_df = pd.read_sql_query(
        return_query,
        conn
    )


    return_rate_df["category"] = (
        return_rate_df["category"]
        .str.title()
    )


    # --------------------------------------------------------
    # CHARTS
    # --------------------------------------------------------

    st.subheader(
        "📈 Revenue Analysis"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.write(
            "**Monthly Net Revenue**"
        )

        st.line_chart(
            monthly_revenue.set_index(
                "month"
            )["net_revenue"]
        )


    with col2:

        st.write(
            "**Revenue by Category**"
        )

        st.bar_chart(
            category_revenue.set_index(
                "category"
            )["net_revenue"]
        )


    col3, col4 = st.columns(2)


    with col3:

        st.write(
            "**Revenue by City**"
        )

        st.bar_chart(
            city_revenue.set_index(
                "city"
            )["net_revenue"]
        )


    with col4:

        st.write(
            "**Return Rate by Category (%)**"
        )

        st.bar_chart(
            return_rate_df.set_index(
                "category"
            )["return_rate"]
        )


    # --------------------------------------------------------
    # INSIGHTS
    # --------------------------------------------------------

    st.subheader(
        "💡 Key Business Insights"
    )


    st.success(
        "📱 Electronics is the largest "
        "revenue-generating product category."
    )


    st.info(
        "🌍 Karachi generates the highest "
        "city-level revenue, followed by Lahore."
    )


    st.warning(
        "↩️ Fashion has the highest return rate. "
        "Product sizing, quality and descriptions "
        "may require further investigation."
    )


# ============================================================
# CHURN PREDICTION
# ============================================================

elif page == "👥 Churn Prediction":

    st.header(
        "👥 Customer Churn Prediction"
    )


    st.write(
        "Predict whether a customer is likely "
        "to stop purchasing."
    )


    st.info(
        "Churn = customer did not purchase "
        "during the target period."
    )


    col1, col2 = st.columns(2)


    with col1:

        st.subheader(
            "🛒 Purchase Behaviour"
        )


        total_orders_input = st.number_input(
            "Total Orders",
            min_value=1,
            value=10,
            step=1
        )


        total_spending = st.number_input(
            "Total Spending",
            min_value=0.0,
            value=50000.0,
            step=1000.0
        )


        average_order_value = st.number_input(
            "Average Order Value",
            min_value=0.0,
            value=5000.0,
            step=100.0
        )


        days_since_last_order = st.number_input(
            "Days Since Last Order",
            min_value=0,
            value=30,
            step=1
        )


    with col2:

        st.subheader(
            "👤 Customer Profile"
        )


        return_rate = st.slider(
            "Return Rate",
            min_value=0.0,
            max_value=1.0,
            value=0.05,
            step=0.01
        )


        average_delivery_days = st.number_input(
            "Average Delivery Days",
            min_value=0.0,
            value=4.0,
            step=0.5
        )


        age = st.number_input(
            "Customer Age",
            min_value=18,
            max_value=100,
            value=30,
            step=1
        )


        membership_type = st.selectbox(
            "Membership Type",
            membership_options
        )


    st.write("")


    if st.button(
        "🔮 Predict Customer Churn"
    ):


        customer_data = pd.DataFrame({

            "total_orders": [
                total_orders_input
            ],

            "total_spending": [
                total_spending
            ],

            "return_rate": [
                return_rate
            ],

            "average_delivery_days": [
                average_delivery_days
            ],

            "average_order_value": [
                average_order_value
            ],

            "days_since_last_order": [
                days_since_last_order
            ],

            "age": [
                age
            ],

            "membership_type": [
                membership_type
            ]

        })


        try:

            prediction = churn_model.predict(
                customer_data
            )[0]


            probability = churn_model.predict_proba(
                customer_data
            )[0][1]


            st.subheader(
                "🎯 Prediction Result"
            )


            if prediction == 1:

                st.error(
                    "⚠️ HIGH CHURN RISK"
                )

                st.metric(
                    "Churn Probability",
                    f"{probability * 100:.2f}%"
                )

                st.write(
                    "This customer is predicted "
                    "to churn."
                )


            else:

                st.success(
                    "✅ CUSTOMER LIKELY TO STAY"
                )

                st.metric(
                    "Churn Probability",
                    f"{probability * 100:.2f}%"
                )

                st.write(
                    "This customer is predicted "
                    "to remain active."
                )


        except Exception as e:

            st.error(
                f"Prediction error: {e}"
            )


# ============================================================
# SENTIMENT ANALYSIS
# ============================================================

elif page == "💬 Sentiment Analysis":

    st.header(
        "💬 Customer Review Sentiment Analysis"
    )


    st.write(
        "Classify customer reviews as "
        "Positive, Neutral or Negative."
    )


    st.info(
        "Sentiment analysis uses TF-IDF "
        "and Logistic Regression."
    )


    review_text = st.text_area(
        "✍️ Enter Customer Review",
        placeholder="Example: The product was excellent.",
        height=180
    )


    if st.button(
        "✨ Analyse Sentiment"
    ):


        if review_text.strip() == "":

            st.warning(
                "Please enter a review first."
            )


        else:

            try:

                sentiment = sentiment_model.predict(
                    [review_text]
                )[0]


                st.subheader(
                    "🎯 Sentiment Result"
                )


                if sentiment == "Positive":

                    st.success(
                        "😊 POSITIVE SENTIMENT"
                    )

                    st.write(
                        "The review indicates a "
                        "positive customer experience."
                    )


                elif sentiment == "Negative":

                    st.error(
                        "😞 NEGATIVE SENTIMENT"
                    )

                    st.write(
                        "The review indicates "
                        "customer dissatisfaction."
                    )


                else:

                    st.warning(
                        "😐 NEUTRAL SENTIMENT"
                    )

                    st.write(
                        "The review expresses "
                        "neutral sentiment."
                    )


            except Exception as e:

                st.error(
                    f"Sentiment prediction error: {e}"
                )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    '<p class="footer">🛍️ ShopSphere Analytics | '
    'Data Science Final Hackathon | '
    'Developed by <b>Sumbal Zaheer</b></p>',
    unsafe_allow_html=True
)