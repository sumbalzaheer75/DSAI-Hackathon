import streamlit as st
import pandas as pd
import sqlite3
import joblib


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ShopSphere Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROFESSIONAL CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(
        135deg,
        #faf7ff 0%,
        #fff9fc 50%,
        #f7f9ff 100%
    );
}

/* Main headings */
h1, h2, h3 {
    color: #32146b !important;
}

/* Normal text */
p {
    color: #334155;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #24104f 0%,
        #3b176f 100%
    );
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* KPI metric cards */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e9ddff;
    border-top: 5px solid #7c3aed;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0px 6px 18px rgba(40, 20, 80, 0.08);
}

[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #32146b !important;
    font-weight: 800;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(
        90deg,
        #7c3aed,
        #a855f7,
        #db2777
    );

    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 10px 24px;
    font-weight: 700;
}

.stButton > button:hover {
    color: white !important;
    border: none;
    box-shadow: 0px 6px 18px rgba(124, 58, 237, 0.25);
}

/* Inputs */
input,
textarea {
    background-color: white !important;
    color: #111827 !important;
}

/* Select box */
[data-baseweb="select"] > div {
    background-color: white !important;
    color: #111827 !important;
}

/* Information boxes */
[data-testid="stAlert"] {
    border-radius: 14px;
}

/* Fix success text */
div[data-testid="stAlert"][data-baseweb="notification"] {
    color: #1f2937 !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #64748b;
    font-size: 14px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD SAVED MODELS
# ============================================================

@st.cache_resource
def load_models():

    churn_model = joblib.load(
        "churn_model.pkl"
    )

    sentiment_model = joblib.load(
        "sentiment_model.pkl"
    )

    return churn_model, sentiment_model


try:

    churn_model, sentiment_model = load_models()

except Exception as e:

    st.error(
        "Models could not be loaded. "
        "Make sure churn_model.pkl and "
        "sentiment_model.pkl are in the same folder as app.py."
    )

    st.exception(e)
    st.stop()


# ============================================================
# DATABASE CONNECTION
# ============================================================

@st.cache_resource
def connect_database():

    return sqlite3.connect(
        "ecommerce_hackathon.db",
        check_same_thread=False
    )


try:

    conn = connect_database()

except Exception as e:

    st.error(
        "Database could not be opened. "
        "Make sure ecommerce_hackathon.db "
        "is in the same folder as app.py."
    )

    st.exception(e)
    st.stop()


# ============================================================
# GET MEMBERSHIP TYPES
# ============================================================

try:

    membership_query = """
    SELECT DISTINCT membership_type
    FROM customers
    WHERE membership_type IS NOT NULL
    ORDER BY membership_type;
    """

    membership_df = pd.read_sql_query(
        membership_query,
        conn
    )

    membership_options = (
        membership_df["membership_type"]
        .astype(str)
        .str.strip()
        .drop_duplicates()
        .tolist()
    )

except Exception as e:

    st.error(
        "Membership types could not be loaded."
    )

    st.exception(e)
    st.stop()


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

st.write(
    "### E-Commerce Customer Intelligence System"
)

st.caption(
    "Business Analytics • Customer Churn • Review Sentiment"
)

st.divider()


# ============================================================
# PAGE 1 - DASHBOARD
# ============================================================

if page == "📊 Dashboard":

    st.header(
        "📊 Business Dashboard"
    )

    st.write(
        "Monitor revenue, customers, orders "
        "and product performance."
    )


    # ========================================================
    # SQL KPI QUERIES
    # ========================================================

    revenue_query = """
    SELECT
        SUM(
            quantity *
            unit_price *
            (1 - discount)
        ) AS net_revenue
    FROM orders
    WHERE quantity > 0
      AND unit_price > 0
      AND date(order_date) IS NOT NULL;
    """


    orders_query = """
    SELECT
        COUNT(*) AS valid_orders
    FROM orders
    WHERE quantity > 0
      AND unit_price > 0
      AND date(order_date) IS NOT NULL;
    """


    customers_query = """
    SELECT
        COUNT(*) AS total_customers
    FROM customers;
    """


    products_query = """
    SELECT
        COUNT(*) AS total_products
    FROM products;
    """


    net_revenue = pd.read_sql_query(
        revenue_query,
        conn
    ).iloc[0]["net_revenue"]


    valid_orders = pd.read_sql_query(
        orders_query,
        conn
    ).iloc[0]["valid_orders"]


    total_customers = pd.read_sql_query(
        customers_query,
        conn
    ).iloc[0]["total_customers"]


    total_products = pd.read_sql_query(
        products_query,
        conn
    ).iloc[0]["total_products"]


    # ========================================================
    # KPI CARDS
    # ========================================================

    st.subheader(
        "📌 Business Overview"
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            label="💰 Net Revenue",
            value=f"{net_revenue / 1_000_000:.1f}M"
        )


    with col2:

        st.metric(
            label="📦 Valid Orders",
            value=f"{valid_orders:,}"
        )


    with col3:

        st.metric(
            label="👥 Customers",
            value=f"{total_customers:,}"
        )


    with col4:

        st.metric(
            label="🛒 Products",
            value=f"{total_products:,}"
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

    ORDER BY month;
    """


    monthly_revenue = pd.read_sql_query(
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
        net_revenue DESC;
    """


    category_revenue = pd.read_sql_query(
        category_query,
        conn
    )


    category_revenue["category"] = (
        category_revenue["category"]
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
        net_revenue DESC;
    """


    city_revenue = pd.read_sql_query(
        city_query,
        conn
    )


    city_revenue["city"] = (
        city_revenue["city"]
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
        return_rate DESC;
    """


    return_rate_df = pd.read_sql_query(
        return_query,
        conn
    )


    return_rate_df["category"] = (
        return_rate_df["category"]
        .str.title()
    )


    # ========================================================
    # CHARTS
    # ========================================================

    st.subheader(
        "📈 Revenue Analysis"
    )


    chart1, chart2 = st.columns(2)


    with chart1:

        st.write(
            "**Monthly Net Revenue Trend**"
        )

        st.line_chart(
            monthly_revenue.set_index(
                "month"
            )["net_revenue"]
        )


    with chart2:

        st.write(
            "**Revenue by Product Category**"
        )

        st.bar_chart(
            category_revenue.set_index(
                "category"
            )["net_revenue"]
        )


    st.write("")


    chart3, chart4 = st.columns(2)


    with chart3:

        st.write(
            "**Revenue by City**"
        )

        st.bar_chart(
            city_revenue.set_index(
                "city"
            )["net_revenue"]
        )


    with chart4:

        st.write(
            "**Return Rate by Category (%)**"
        )

        st.bar_chart(
            return_rate_df.set_index(
                "category"
            )["return_rate"]
        )


    # ========================================================
    # BUSINESS INSIGHTS
    # ========================================================

    st.subheader(
        "💡 Key Business Insights"
    )


    st.markdown(
        """
        **📱 Electronics — Revenue Leader**

        Electronics is the largest revenue-generating
        product category and is a major contributor
        to overall business performance.
        """
    )


    st.markdown(
        """
        **🌍 Karachi — Strongest Market**

        Karachi generates the highest city-level
        revenue, followed by Lahore, making these
        important markets for the business.
        """
    )


    st.markdown(
        """
        **↩️ Fashion — Highest Return Rate**

        Fashion has the highest product return rate.
        Product quality, sizing, descriptions and
        customer expectations may require further
        investigation.
        """
    )


# ============================================================
# PAGE 2 - CHURN PREDICTION
# ============================================================

elif page == "👥 Churn Prediction":

    st.header(
        "👥 Customer Churn Prediction"
    )

    st.write(
        "Identify customers who may stop purchasing "
        "so retention action can be taken early."
    )


    st.info(
        "The churn model uses historical customer "
        "behaviour such as orders, spending, recency, "
        "returns, delivery time, age and membership."
    )


    col1, col2 = st.columns(2)


    # ========================================================
    # PURCHASE BEHAVIOUR
    # ========================================================

    with col1:

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
    # CUSTOMER PROFILE
    # ========================================================

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


    # ========================================================
    # CHURN PREDICTION BUTTON
    # ========================================================

    if st.button(
        "🔮 Predict Customer Churn",
        key="churn_button"
    ):


        customer_data = pd.DataFrame({

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
                    label="Churn Probability",
                    value=f"{probability * 100:.2f}%"
                )


                st.write(
                    "This customer is predicted to churn. "
                    "The business may consider targeted "
                    "retention offers or engagement."
                )


            else:

                st.success(
                    "✅ CUSTOMER LIKELY TO STAY"
                )


                st.metric(
                    label="Churn Probability",
                    value=f"{probability * 100:.2f}%"
                )


                st.write(
                    "The model predicts that this customer "
                    "is likely to remain active."
                )


        except Exception as e:

            st.error(
                "Churn prediction could not be completed."
            )

            st.exception(e)


# ============================================================
# PAGE 3 - SENTIMENT ANALYSIS
# ============================================================

elif page == "💬 Sentiment Analysis":

    st.header(
        "💬 Customer Review Sentiment Analysis"
    )


    st.write(
        "Analyse customer feedback and classify "
        "reviews as Positive, Neutral or Negative."
    )


    st.info(
        "The sentiment model uses TF-IDF text features "
        "with Logistic Regression to classify "
        "customer reviews."
    )


    review_text = st.text_area(
        "✍️ Enter Customer Review",
        placeholder=(
            "Example: The product quality was excellent "
            "and delivery was very fast."
        ),
        height=180
    )


    if st.button(
        "✨ Analyse Sentiment",
        key="sentiment_button"
    ):


        if review_text.strip() == "":

            st.warning(
                "Please enter a customer review first."
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
                        "The review indicates a positive "
                        "customer experience."
                    )


                elif sentiment == "Negative":

                    st.error(
                        "😞 NEGATIVE SENTIMENT"
                    )

                    st.write(
                        "The review indicates customer "
                        "dissatisfaction and may require "
                        "attention."
                    )


                else:

                    st.warning(
                        "😐 NEUTRAL SENTIMENT"
                    )

                    st.write(
                        "The review expresses neither "
                        "strongly positive nor strongly "
                        "negative sentiment."
                    )


            except Exception as e:

                st.error(
                    "Sentiment analysis could not "
                    "be completed."
                )

                st.exception(e)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <p class="footer">
        🛍️ ShopSphere Analytics
        &nbsp; | &nbsp;
        Data Science Final Hackathon
        &nbsp; | &nbsp;
        Developed by <b>Sumbal Zaheer</b>
    </p>
    """,
    unsafe_allow_html=True
)