import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

def fetch_evaluations():
    try:
        response = requests.get("http://localhost:8000/evaluations")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to fetch evaluations: {str(e)}")
        return []

def display_evaluation_charts():
    evaluations = fetch_evaluations()
    if not evaluations:
        st.info("No evaluation data available.")
        return

    # Create DataFrame
    df = pd.DataFrame(evaluations)

    # Check if 'metrics' column exists and is a dictionary
    if 'metrics' in df.columns and isinstance(df.at[0, 'metrics'], dict):
        # Expand 'metrics' dictionary into separate columns
        metrics_df = pd.json_normalize(df['metrics'])
        df = pd.concat([df.drop('metrics', axis=1), metrics_df], axis=1)
    else:
        st.error("Metrics data is not in the expected format.")
        return

    # Ensure all metric columns are numeric
    metric_columns = ['response_time', 'tokens_used', 'relevance_score', 'citation_accuracy']
    for col in metric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    st.header("Model Performance Evaluation")

    # Response Time Comparison
    st.subheader("Response Time (seconds)")
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='model', y='response_time', data=df)
    plt.title('Response Time by Model')
    st.pyplot(plt)

    # Token Usage Comparison
    st.subheader("Token Usage")
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='model', y='tokens_used', data=df)
    plt.title('Token Usage by Model')
    st.pyplot(plt)

    # Relevance Score Comparison
    st.subheader("Relevance Score")
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='model', y='relevance_score', data=df)
    plt.title('Relevance Score by Model')
    st.pyplot(plt)

    # Citation Accuracy Comparison
    st.subheader("Citation Accuracy")
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='model', y='citation_accuracy', data=df)
    plt.title('Citation Accuracy by Model')
    st.pyplot(plt)

    # Average Metrics
    st.subheader("Average Metrics")
    avg_metrics = df.groupby('model')[metric_columns].mean().reset_index()
    st.dataframe(avg_metrics)

    # Correlation Heatmap
    st.subheader("Correlation Between Metrics")
    corr = avg_metrics[metric_columns].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('Correlation Heatmap')
    st.pyplot(plt)