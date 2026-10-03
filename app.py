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
# FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "ecommerce_hackathon.db"
CHURN_MODEL_PATH = BASE_DIR / "churn_model.pkl"
SENTIMENT_MODEL_PATH = BASE_DIR / "sentiment_model.pkl"


# ============================================================
# SIMPLE SAFE CSS
# ============================================================

st.markdown("""
<style>

/* Page */
.stApp {
    background-color: #faf8ff;
}

/* Headings */
h1, h2, h3 {
    color: #4c1d95 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #4c1d95;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: white !important;
}

/* INPUT LABELS */
[data-testid="stWidgetLabel"] p {
    color: #1f2937 !important;
    font-weight: 600 !important;
}

/* NUMBER INPUT */
[data-testid="stNumberInput"] input {
    background-color: white !important;
    color: #111827 !important;
}

/* TEXT AREA */
[data-testid="stTextArea"] textarea {
    background-color: white !important;
    color: #111827 !important;
}

/* SELECT BOX */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: white !important;
    color: #111827 !important;
}

/* Metric */
[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #ddd6fe;
}

[data-testid="stMetricLabel"] p {
    color: #475569 !important;
}

[data-testid="stMetricValue"] {
    color: #4c1d95 !important;
}

/* Buttons */
.stButton > button {
    background-color: #7c3aed;
    color: white !important;
    border-radius: 10px;
    border: none;
    font-weight: 600;
}

/* Alert text */
[data-testid="stAlert"] p {
    color: #1f2937 !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #64748b;
    padding: 15px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD MODELS
# ============================================================

@st.cache_resource
def load_models():

    churn = joblib.load(
        CHURN_MODEL_PATH
    )

    sentiment = joblib.load(
        SENTIMENT_MODEL_PATH
    )

    return churn, sentiment


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
def get_connection():

    return sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )


try:

    conn = get_connection()

except Exception as e:

    st.error(
        f"Database error: {e}"
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
# MAIN HEADER
# ============================================================

st.title(
    "🛍️ ShopSphere Analytics"
)

st.subheader(
    "E-Commerce Customer Intelligence System"
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
        "Monitor key e-commerce business performance."
    )


    # ========================================================
    # KPIs
    # ========================================================

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


    revenue = pd.read_sql_query(
        revenue_query,
        conn
    ).iloc[0]["net_revenue"]


    orders = pd.read_sql_query(
        orders_query,
        conn
    ).iloc[0]["total_orders"]


    customers = pd.read_sql_query(
        customers_query,
        conn
    ).iloc[0]["total_customers"]


    products = pd.read_sql_query(
        products_query,
        conn
    ).iloc[0]["total_products"]


    c1, c2, c3, c4 = st.columns(4)


    c1.metric(
        "💰 Net Revenue",
        f"{revenue / 1000000:.1f}M"
    )


    c2.metric(
        "📦 Valid Orders",
        f"{orders:,}"
    )


    c3.metric(
        "👥 Customers",
        f"{customers:,}"
    )


    c4.metric(
        "🛒 Products",
        f"{products:,}"
    )


    st.write("")


    # ========================================================
    # MONTHLY REVENUE
    # ========================================================

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


    monthly_df = pd.read_sql_query(
        monthly_query,
        conn
    )


    # ========================================================
    # CATEGORY REVENUE
    # ========================================================

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


    category_df = pd.read_sql_query(
        category_query,
        conn
    )


    category_df["category"] = (
        category_df["category"]
        .str.title()
    )


    # ========================================================
    # CITY REVENUE
    # ========================================================

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


    city_df = pd.read_sql_query(
        city_query,
        conn
    )


    city_df["city"] = (
        city_df["city"]
        .str.title()
    )


    # ========================================================
    # RETURN RATE
    # ========================================================

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


    return_df = pd.read_sql_query(
        return_query,
        conn
    )


    return_df["category"] = (
        return_df["category"]
        .str.title()
    )


    # ========================================================
    # CHARTS
    # ========================================================

    st.subheader(
        "📈 Revenue Analysis"
    )


    left, right = st.columns(2)


    with left:

        st.write(
            "**Monthly Net Revenue**"
        )

        st.line_chart(
            monthly_df.set_index(
                "month"
            )["net_revenue"]
        )


    with right:

        st.write(
            "**Revenue by Category**"
        )

        st.bar_chart(
            category_df.set_index(
                "category"
            )["net_revenue"]
        )


    left, right = st.columns(2)


    with left:

        st.write(
            "**Revenue by City**"
        )

        st.bar_chart(
            city_df.set_index(
                "city"
            )["net_revenue"]
        )


    with right:

        st.write(
            "**Return Rate by Category (%)**"
        )

        st.bar_chart(
            return_df.set_index(
                "category"
            )["return_rate"]
        )


    # ========================================================
    # INSIGHTS
    # ========================================================

    st.subheader(
        "💡 Business Insights"
    )


    st.success(
        "Electronics is the highest revenue-generating "
        "product category."
    )


    st.info(
        "Karachi generates the highest city-level "
        "revenue, followed by Lahore."
    )


    st.warning(
        "Fashion has the highest return rate, "
        "indicating an area for further investigation."
    )


# ============================================================
# CHURN PAGE
# ============================================================

elif page == "👥 Churn Prediction":

    st.header(
        "👥 Customer Churn Prediction"
    )


    st.write(
        "Enter customer information to estimate "
        "the probability of churn."
    )


    st.info(
        "Positive churn class means the customer "
        "is predicted to stop purchasing."
    )


    left, right = st.columns(2)


    # ========================================================
    # LEFT COLUMN
    # ========================================================

    with left:

        st.subheader(
            "🛒 Purchase Behaviour"
        )


        total_orders = st.number_input(
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


    # ========================================================
    # RIGHT COLUMN
    # ========================================================

    with right:

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


    # ========================================================
    # CHURN PREDICTION
    # ========================================================

    if st.button(
        "🔮 Predict Customer Churn",
        type="primary"
    ):


        input_data = pd.DataFrame({

            "total_orders": [
                total_orders
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
                input_data
            )[0]


            probability = churn_model.predict_proba(
                input_data
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


            else:

                st.success(
                    "✅ CUSTOMER LIKELY TO STAY"
                )

                st.metric(
                    "Churn Probability",
                    f"{probability * 100:.2f}%"
                )


        except Exception as e:

            st.error(
                f"Prediction error: {e}"
            )


# ============================================================
# SENTIMENT PAGE
# ============================================================

elif page == "💬 Sentiment Analysis":

    st.header(
        "💬 Customer Review Sentiment Analysis"
    )


    st.write(
        "Enter a customer review to classify "
        "its sentiment."
    )


    st.info(
        "Sentiment analysis uses TF-IDF "
        "and Logistic Regression."
    )


    review = st.text_area(
        "Customer Review",
        placeholder="Example: This product is very good.",
        height=160
    )


    if st.button(
        "✨ Analyse Sentiment",
        type="primary"
    ):


        if not review.strip():

            st.warning(
                "Please enter a review."
            )


        else:

            try:

                prediction = sentiment_model.predict(
                    [review]
                )[0]


                st.subheader(
                    "🎯 Sentiment Result"
                )


                if prediction == "Positive":

                    st.success(
                        "😊 POSITIVE"
                    )


                elif prediction == "Negative":

                    st.error(
                        "😞 NEGATIVE"
                    )


                else:

                    st.warning(
                        "😐 NEUTRAL"
                    )


            except Exception as e:

                st.error(
                    f"Prediction error: {e}"
                )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    '<p class="footer">'
    '🛍️ ShopSphere Analytics | '
    'Data Science Final Hackathon | '
    'Developed by <b>Sumbal Zaheer</b>'
    '</p>',
    unsafe_allow_html=True
)