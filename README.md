# 🛍️ ShopSphere Analytics
### E-Commerce Customer Intelligence System

**Data Science Final Hackathon**  
**Developed by: Sumbal Zaheer**

🔗 **Live Application:**  
https://sumbalzaheer75-dsai-hackathon-app-aqt0qg.streamlit.app/

---

## 📌 Project Overview

ShopSphere Analytics is an end-to-end Data Science project developed to analyse e-commerce customer behaviour and support business decision-making.

The project uses an SQLite e-commerce database containing approximately **100,000 records** across four tables:

- Customers
- Products
- Orders
- Reviews

The complete solution includes:

- Data Inspection and Cleaning
- SQL Business Analysis
- Exploratory Data Analysis
- Customer Churn Prediction
- Deep Learning
- Customer Review Sentiment Analysis
- Streamlit Deployment

---

## 🧹 Data Cleaning

The dataset was inspected for:

- Missing values
- Duplicate records
- Invalid numerical values
- Invalid dates
- Invalid review ratings
- Inconsistent text values
- Missing review text

Cleaning included median and mode imputation, text standardisation, date conversion, validation of ratings, and removal of invalid transaction records where required.

---

## 💾 SQL Business Analysis

SQL queries were executed directly against the SQLite database to analyse:

1. Total Net Revenue
2. Top 10 Customers by Spending
3. Revenue, Orders and Quantity by Category
4. Monthly Net Revenue
5. Top 5 Products by Net Revenue

The business generated approximately **936 million in net revenue**.

---

## 📊 Exploratory Data Analysis

The project includes four main business visualisations:

- Monthly Revenue Trend
- Revenue by Product Category
- Revenue by City
- Return Rate by Category

### 💡 Key Business Insights

**1. Electronics is the strongest revenue category**  
Electronics generated approximately **656 million** in net revenue and was the largest contributor to overall revenue.

**2. Karachi is the highest-revenue city**  
Karachi generated approximately **244.6 million** in revenue, followed by Lahore.

**3. Fashion has the highest return rate**  
The Fashion category showed the highest return rate, suggesting that areas such as sizing, product quality, descriptions and customer expectations may require further investigation.

---

## 👥 Customer Churn Prediction

Customer churn was predicted using historical customer purchasing behaviour.

Historical features were created using orders up to **31 May 2026**.

The target period was:

**1 June 2026 – 31 August 2026**

A customer was classified as:

- **Churn = 1:** No purchase during the target period
- **Churn = 0:** Customer purchased during the target period

### Features Used

- Total Orders
- Total Spending
- Average Order Value
- Days Since Last Order
- Return Rate
- Average Delivery Days
- Age
- Membership Type

### Models Compared

Two Machine Learning models were evaluated:

- Logistic Regression
- Random Forest

### Logistic Regression Results

| Metric | Score |
|---|---:|
| Accuracy | 71.54% |
| Precision | 66.67% |
| Recall | 83.93% |
| F1 Score | 74.31% |
| ROC-AUC | 78.72% |

### Random Forest Results

| Metric | Score |
|---|---:|
| Accuracy | 69.85% |
| Precision | 67.13% |
| Recall | 75.51% |
| F1 Score | 71.07% |
| ROC-AUC | 76.23% |

**Logistic Regression was selected as the final churn model** because it provided stronger overall performance and higher recall for identifying customers at risk of churn.

The trained model was saved as:

`churn_model.pkl`

---

## 🧠 Deep Learning

A Neural Network was also developed with the following architecture:

**Input → Dense(32, ReLU) → Dense(16, ReLU) → Dense(1, Sigmoid)**

### Neural Network Results

| Metric | Score |
|---|---:|
| Accuracy | 69.17% |
| Precision | 66.53% |
| Recall | 74.73% |
| F1 Score | 70.39% |
| ROC-AUC | 77.66% |

The Neural Network did not provide a significant advantage over Logistic Regression. Therefore, the simpler Logistic Regression model was preferred for deployment.

---

## 💬 Sentiment Analysis

Customer reviews were classified into three sentiment categories based on ratings:

- **1–2 → Negative**
- **3 → Neutral**
- **4–5 → Positive**

The NLP pipeline uses:

**Review Text → TF-IDF Vectorisation → Logistic Regression → Sentiment Prediction**

The final model predicts:

- 😊 Positive
- 😐 Neutral
- 😞 Negative

The trained sentiment model was saved as:

`sentiment_model.pkl`

---

## 🌐 Streamlit Application

The final solution was deployed as an interactive Streamlit application.

### 🔗 Live App

**https://sumbalzaheer75-dsai-hackathon-app-aqt0qg.streamlit.app/**

The application contains three sections:

### 📊 Business Dashboard

Displays:

- Net Revenue
- Valid Orders
- Total Customers
- Total Products
- Monthly Revenue
- Category Revenue
- City Revenue
- Return Rate by Category
- Business Insights

The dashboard executes SQL queries directly against the SQLite database.

### 👥 Churn Prediction

Users can enter customer characteristics and receive:

- Churn / Stay Prediction
- Churn Probability

The application uses the saved `churn_model.pkl`.

### 💬 Sentiment Analysis

Users can enter customer review text and receive:

- Positive
- Neutral
- Negative

The application uses the saved `sentiment_model.pkl`.

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- SQLite / SQL
- Scikit-learn
- Logistic Regression
- Random Forest
- TensorFlow / Keras
- Neural Networks
- TF-IDF
- Natural Language Processing
- Matplotlib
- Streamlit
- Joblib
- GitHub

---

## 📂 Project Files

```text
DSAI Hackthon.ipynb
app.py
business_queries.sql
ecommerce_hackathon.db
churn_model.pkl
sentiment_model.pkl
requirements.txt
README.md
```

---

## 🎯 Conclusion

ShopSphere Analytics demonstrates a complete end-to-end Data Science workflow, starting from raw SQLite data and progressing through cleaning, SQL analysis, visualisation, Machine Learning, Deep Learning and NLP.

The project identified important business patterns including strong Electronics revenue, high revenue contribution from Karachi, and a higher return rate in Fashion.

A Logistic Regression model was selected for customer churn prediction, while TF-IDF with Logistic Regression was used for customer sentiment classification.

Both trained models were integrated into a deployed Streamlit application, allowing business analytics and predictive models to be accessed through an interactive interface.

---

## 👩‍💻 Author

**Sumbal Zaheer**  
Data Science Final Hackathon

🌐 **Live App:**  
https://sumbalzaheer75-dsai-hackathon-app-aqt0qg.streamlit.app/
