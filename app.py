import json
import os
import streamlit as st
from sentence_transformers import SentenceTransformer

from src.rag_pipeline import (
    extract_uploaded_pdf,
    create_uploaded_chunks,
    extract_financial_metrics,
    ask_uploaded_report
)

from src.analytics import calculate_financial_ratios


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="InvestIQ",
    page_icon="📊",
    layout="wide"
)
st.markdown("""
<style>

.stApp {
    background: #0b0f19;
    color: #f5f7fa;
}

section[data-testid="stSidebar"] {
    background: #111827;
}

h1, h2, h3 {
    color: #f8fafc;
}

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #111827, #0f172a);
    border: 1px solid #273244;
    padding: 20px;
    border-radius: 16px;
    min-height: 110px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
}

div[data-testid="stMetricLabel"] {
    color: #9ca3af;
}

div[data-testid="stMetricValue"] {
    color: #f8fafc;
}

.stButton > button {
    border-radius: 10px;
    border: 1px solid #374151;
}

</style>
""", unsafe_allow_html=True)
GROQ_API_KEY = os.environ.get(
    "GROQ_API_KEY"
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    '<div style="padding:10px 0 24px 0;">'
    '<div style="font-size:42px;font-weight:800;letter-spacing:-1px;">'
    '📊 InvestIQ'
    '</div>'
    '<div style="font-size:18px;color:#9ca3af;margin-top:4px;">'
    'AI-powered Annual Report Intelligence'
    '</div>'
    '<div style="font-size:14px;color:#6b7280;margin-top:8px;">'
    'Upload a company annual report to extract financial insights, '
    'calculate key ratios, and ask questions with cited evidence.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    "AI-powered Annual Report Intelligence"
)

st.divider()


# --------------------------------------------------
# Upload annual report
# --------------------------------------------------



st.markdown(
    '<div style="background:#111827;border:1px solid #1f2937;'
    'border-radius:16px;padding:22px;margin:10px 0 24px 0;">'
    '<div style="font-size:20px;font-weight:700;color:#f8fafc;">'
    '📄 Upload Annual Report'
    '</div>'
    '<div style="font-size:14px;color:#9ca3af;margin-top:6px;">'
    'Upload a company annual report PDF to begin your analysis.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

uploaded_report = st.file_uploader(
    "Choose an annual report PDF",
    type=["pdf"],
    label_visibility="collapsed"
)

# --------------------------------------------------
# Process uploaded report
# --------------------------------------------------

if uploaded_report is not None:

    st.session_state["uploaded_report"] = uploaded_report

    with st.spinner("Processing annual report..."):
        pages = extract_uploaded_pdf(
            uploaded_report
        )

        chunks = create_uploaded_chunks(
            pages
        )

        metrics = extract_financial_metrics(
            pages
        )

        embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        chunk_texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = embedding_model.encode(
            chunk_texts,
            show_progress_bar=False
        )

        st.session_state["uploaded_pages"] = pages
        st.session_state["uploaded_chunks"] = chunks
        st.session_state["uploaded_embeddings"] = embeddings
        st.session_state["uploaded_embedding_model"] = embedding_model

        ratios = calculate_financial_ratios(
            metrics
        )

        with open(
            "/content/investiq/data/current_financial_metrics.json",
            "w"
        ) as f:

            json.dump(
                metrics,
                f,
                indent=2
            )

    st.success(
        f"✅ Report processed successfully — "
        f"{len(pages)} pages analyzed"
    )

else:

    metrics = {
        "Revenue": None,
        "Net Income": None,
        "Operating Income": None,
        "Operating Cash Flow": None,
        "Total Assets": None,
        "Total Liabilities": None,
        "Total Equity": None,
        "Cash & Equivalents": None,
        "Long-Term Debt": None
    }

    ratios = {}


st.divider()


# --------------------------------------------------
# Financial overview
# --------------------------------------------------

st.subheader("📊 Financial Overview")

if uploaded_report is not None:

    st.write(
        f"Financial metrics extracted from "
        f"**{uploaded_report.name}**"
    )

else:

    st.info(
        "Upload an annual report PDF to begin analysis."
    )


# --------------------------------------------------
# KPI cards
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Revenue",
        f"${metrics['Revenue']:,.0f}M"
        if metrics["Revenue"] is not None
        else "—"
    )

with col2:
    st.metric(
        "Net Income",
        f"${metrics['Net Income']:,.0f}M"
        if metrics["Net Income"] is not None
        else "—"
    )

with col3:
    st.metric(
        "Operating Income",
        f"${metrics['Operating Income']:,.0f}M"
        if metrics["Operating Income"] is not None
        else "—"
    )


col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Operating Cash Flow",
        f"${metrics['Operating Cash Flow']:,.0f}M"
        if metrics["Operating Cash Flow"] is not None
        else "—"
    )

with col5:
    st.metric(
        "Total Assets",
        f"${metrics['Total Assets']:,.0f}M"
        if metrics["Total Assets"] is not None
        else "—"
    )

with col6:
    st.metric(
        "Total Equity",
        f"${metrics['Total Equity']:,.0f}M"
        if metrics["Total Equity"] is not None
        else "—"
    )


col7, col8, col9 = st.columns(3)

with col7:
    st.metric(
        "Total Liabilities",
        f"${metrics['Total Liabilities']:,.0f}M"
        if metrics["Total Liabilities"] is not None
        else "—"
    )

with col8:
    st.metric(
        "Cash & Equivalents",
        f"${metrics['Cash & Equivalents']:,.0f}M"
        if metrics["Cash & Equivalents"] is not None
        else "—"
    )

with col9:
    st.metric(
        "Long-Term Debt",
        f"${metrics['Long-Term Debt']:,.0f}M"
        if metrics["Long-Term Debt"] is not None
        else "—"
    )


# --------------------------------------------------
# Financial ratios
# --------------------------------------------------

st.divider()

st.subheader("📐 Financial Ratios")

if ratios:
    st.markdown(
        '<div style="font-size:14px;color:#9ca3af;margin-bottom:12px;">'
        'Key profitability and return indicators calculated from the uploaded report.'
        '</div>',
        unsafe_allow_html=True
    )

    ratio_col1, ratio_col2, ratio_col3, ratio_col4 = st.columns(4)

    with ratio_col1:
        st.metric(
            "Net Profit Margin",
            f"{ratios['Net Profit Margin']:.2f}%"
        )

    with ratio_col2:
        st.metric(
            "Operating Margin",
            f"{ratios['Operating Margin']:.2f}%"
        )

    with ratio_col3:
        st.metric(
            "Return on Assets",
            f"{ratios['Return on Assets']:.2f}%"
        )

    with ratio_col4:
        st.metric(
            "Return on Equity",
            f"{ratios['Return on Equity']:.2f}%"
        )

else:

    st.info(
        "Upload an annual report to calculate financial ratios."
    )

# --------------------------------------------------
# Financial performance chart
# --------------------------------------------------

st.divider()

st.subheader("📈 Financial Performance")

if uploaded_report is not None:

    chart_data = {
        "Metric": [
            "Revenue",
            "Operating Income",
            "Net Income"
        ],
        "Amount ($M)": [
            metrics["Revenue"],
            metrics["Operating Income"],
            metrics["Net Income"]
        ]
    }

    st.bar_chart(
    chart_data,
    x="Metric",
    y="Amount ($M)",
    height=350
)

else:

    st.info(
        "Upload an annual report to view financial performance."
    )
# --------------------------------------------------
# Status
# --------------------------------------------------

st.divider()

if uploaded_report is not None:

    st.success(
        "✅ Financial analysis generated dynamically "
        "from the uploaded annual report."
    )
# --------------------------------------------------
# Ask AI
# --------------------------------------------------

st.divider()

st.subheader("🤖 Ask the Annual Report")

if uploaded_report is not None or "uploaded_report" in st.session_state:

    question = st.text_input(
        "Ask a question about the uploaded annual report",
        placeholder="Example: What was the company's revenue in 2025?"
    )

    if question:

        if GROQ_API_KEY is None:

            st.error(
                "GROQ_API_KEY is not available."
            )

        elif "uploaded_chunks" not in st.session_state:

            st.warning(
                "Please upload and process the annual report first."
            )

        else:

            with st.spinner(
                "🔎 Searching the annual report..."
            ):

                answer, sources = ask_uploaded_report(
                    question,
                    st.session_state["uploaded_chunks"],
                    st.session_state["uploaded_embeddings"],
                    st.session_state["uploaded_embedding_model"],
    GROQ_API_KEY,
    top_k=10
)

            st.markdown("### 💡 Answer")

            st.write(answer)

            st.markdown("### 📚 Sources")

            for source in sources:

                with st.expander(
                    f"Page {source['page']} • "
                    f"Similarity: {source['score']:.3f}"
                ):

                    st.write(
                        source["text"]
                    )

else:

    st.info(
        "Upload an annual report to ask questions about it."
    )