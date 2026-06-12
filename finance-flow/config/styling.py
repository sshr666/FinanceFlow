import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        .main > div {
            padding-top: 1rem;
        }

        /* ===== Fintech Dark Theme ===== */

        /* --- Metric Cards --- */
        div[data-testid="metric-container"] {
            background-color: #111827;
            border: 1px solid #1e293b;
            border-radius: 12px;
            padding: 16px 20px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
            transition: border-color 0.2s;
        }
        div[data-testid="metric-container"]:hover {
            border-color: #374151;
        }
        div[data-testid="metric-container"] label {
            color: #94a3b8 !important;
            font-size: 0.8rem !important;
            font-weight: 500 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        div[data-testid="stMetricValue"] {
            color: #f8fafc !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            line-height: 1.2;
            padding-top: 4px;
        }
        div[data-testid="stMetricDelta"] {
            font-size: 0.85rem !important;
            font-weight: 600 !important;
        }
        div[data-testid="stMetricDelta"] svg {
            display: inline !important;
        }

        /* --- Page Titles & Subheaders --- */
        h1 {
            color: #f8fafc !important;
            font-weight: 700 !important;
            font-size: 1.75rem !important;
            margin-bottom: 1.5rem !important;
        }
        h2 {
            color: #f1f5f9 !important;
            font-weight: 600 !important;
            font-size: 1.25rem !important;
            margin-bottom: 1rem !important;
        }
        h3 {
            color: #e2e8f0 !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
        }

        /* --- Dividers --- */
        hr {
            border-color: #1e293b !important;
            margin: 1.5rem 0 !important;
        }

        /* --- Section Cards (for chart areas, transaction lists) --- */
        div.stColumn > div:has(> div.stPlotlyChart),
        .element-container:has(> div.stPlotlyChart) {
            background-color: #111827;
            border: 1px solid #1e293b;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 1rem;
        }

        /* --- Budget Summary Rows --- */
        .budget-card {
            background-color: #111827;
            border: 1px solid #1e293b;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 0.75rem;
            transition: border-color 0.2s;
        }
        .budget-card:hover {
            border-color: #374151;
        }
        .budget-card .budget-category {
            color: #f1f5f9;
            font-weight: 600;
            font-size: 0.95rem;
        }
        .budget-card .budget-spend {
            color: #94a3b8;
            font-size: 0.85rem;
        }
        .budget-alert-warning {
            color: #f97316;
            font-weight: 700;
            font-size: 0.9rem;
        }
        .budget-alert-danger {
            color: #ef4444;
            font-weight: 700;
            font-size: 0.9rem;
        }

        /* --- Progress Bars --- */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #22c55e, #16a34a);
            border-radius: 4px;
        }
        .stProgress > div > div {
            background-color: #1e293b;
            border-radius: 4px;
            height: 8px;
        }

        /* --- Alerts / Info / Success / Warning / Error --- */
        .stAlert {
            background-color: #1e293b !important;
            border: 1px solid #334155 !important;
            border-radius: 10px !important;
            color: #e2e8f0 !important;
        }
        div[data-baseweb="notification"] {
            background-color: #1e293b !important;
            border: 1px solid #334155 !important;
            border-radius: 10px !important;
        }
        .stInfo {
            background-color: #0f172a !important;
            border: 1px solid #1e3a5f !important;
            border-radius: 10px !important;
            color: #93c5fd !important;
        }
        .stSuccess {
            background-color: #0f172a !important;
            border: 1px solid #166534 !important;
            border-radius: 10px !important;
            color: #86efac !important;
        }
        .stWarning {
            background-color: #0f172a !important;
            border: 1px solid #78350f !important;
            border-radius: 10px !important;
            color: #fdba74 !important;
        }
        .stError {
            background-color: #0f172a !important;
            border: 1px solid #7f1d1d !important;
            border-radius: 10px !important;
            color: #fca5a5 !important;
        }

        /* --- Buttons --- */
        .stButton button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.2s;
        }
        .stButton button[kind="primary"] {
            background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
            border: none !important;
            color: white !important;
            box-shadow: 0 1px 3px rgba(59, 130, 246, 0.3);
        }
        .stButton button[kind="primary"]:hover {
            background: linear-gradient(135deg, #60a5fa, #3b82f6) !important;
            box-shadow: 0 2px 6px rgba(59, 130, 246, 0.4);
        }
        .stButton button[kind="secondary"] {
            background-color: #1e293b !important;
            border: 1px solid #334155 !important;
            color: #e2e8f0 !important;
        }
        .stButton button[kind="secondary"]:hover {
            border-color: #475569 !important;
            background-color: #334155 !important;
        }

        /* --- Tabs --- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0;
            background-color: #0f172a;
            border-radius: 10px;
            padding: 4px;
            border: 1px solid #1e293b;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px !important;
            padding: 8px 16px !important;
            color: #94a3b8 !important;
            font-weight: 500 !important;
        }
        .stTabs [aria-selected="true"] {
            background-color: #1e293b !important;
            color: #f8fafc !important;
        }

        /* --- Expanders --- */
        .stExpander {
            background-color: #111827;
            border: 1px solid #1e293b;
            border-radius: 12px;
            margin-bottom: 0.75rem;
        }
        .stExpander details {
            padding: 8px 16px;
        }
        .stExpander summary {
            color: #e2e8f0 !important;
            font-weight: 600;
        }

        /* --- Data Editor / Tables --- */
        div[data-testid="stDataFrame"] {
            background-color: #111827;
            border: 1px solid #1e293b;
            border-radius: 12px;
            padding: 8px;
        }
        div[data-testid="stDataFrame"] table {
            color: #e2e8f0 !important;
        }
        div[data-testid="stDataFrame"] th {
            background-color: #0f172a !important;
            color: #94a3b8 !important;
            font-weight: 600 !important;
            font-size: 0.8rem !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        div[data-testid="stDataFrame"] td {
            color: #f1f5f9 !important;
        }

        /* --- Select Box / Input Fields --- */
        div[data-baseweb="select"] > div {
            background-color: #111827 !important;
            border-color: #1e293b !important;
            border-radius: 8px !important;
        }
        div[data-baseweb="input"] > div {
            background-color: #111827 !important;
            border-color: #1e293b !important;
            border-radius: 8px !important;
        }
        div[data-baseweb="textarea"] textarea {
            background-color: #111827 !important;
            border-color: #1e293b !important;
            border-radius: 8px !important;
            color: #e2e8f0 !important;
        }

        /* --- Sidebar --- */
        section[data-testid="stSidebar"] {
            background-color: #0f172a;
            border-right: 1px solid #1e293b;
        }
        section[data-testid="stSidebar"] .stSelectbox label {
            color: #94a3b8 !important;
        }

        /* --- Number Input --- */
        div[data-baseweb="input"] input {
            color: #f8fafc !important;
        }

        /* --- File Uploader --- */
        section[data-testid="stFileUploader"] {
            background-color: #111827;
            border: 1px dashed #334155;
            border-radius: 12px;
            padding: 16px;
        }

        /* --- Captions --- */
        .stCaption {
            color: #64748b !important;
        }

        /* --- Review Cards --- */
        .review-card {
            background-color: #111827;
            border: 1px solid #1e293b;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            transition: border-color 0.2s;
        }
        .review-card:hover {
            border-color: #374151;
        }
        .review-card .review-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .review-card .review-username {
            color: #f1f5f9;
            font-weight: 600;
            font-size: 0.95rem;
        }
        .review-card .review-date {
            color: #94a3b8;
            font-size: 0.85rem;
        }
        .review-card .review-stars {
            font-size: 1.2rem;
            margin: 4px 0;
        }
        .review-card .review-comment {
            color: #e2e8f0;
            margin: 8px 0 0 0;
            line-height: 1.5;
        }

        /* --- Transaction List (Dashboard) --- */
        .transaction-item {
            padding: 8px 0;
            border-bottom: 1px solid #1e293b;
        }
        .transaction-item:last-child {
            border-bottom: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
