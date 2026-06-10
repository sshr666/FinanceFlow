import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        .main > div {
            padding-top: 1rem;
        }
        .stMetric {
            background-color: #f0f2f6;
            border-radius: 8px;
            padding: 12px;
        }
        .stProgress > div > div > div > div {
            background-color: #4CAF50;
        }
        .budget-alert-warning {
            color: #ff9800;
            font-weight: bold;
        }
        .budget-alert-danger {
            color: #f44336;
            font-weight: bold;
        }
        div[data-testid="stMetricValue"] {
            font-size: 1.8rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
