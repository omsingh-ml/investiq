# InvestIQ

🚀 **Launch InvestIQ Live Demo:** https://investiq-jkrfpgksbhbfdupeappuqk.streamlit.app/

AI-powered Annual Report Intelligence Platform.

InvestIQ allows users to upload a company annual report PDF and:

- Extract key financial metrics
- Calculate financial ratios
- Visualize financial performance
- Ask questions about the uploaded report
- Retrieve relevant evidence using semantic search
- Generate answers with page citations
- Avoid hallucinating information that is not present in the report

## Features

### Financial Analysis

Extracts:

- Revenue
- Net Income
- Operating Income
- Operating Cash Flow
- Total Assets
- Total Liabilities
- Total Equity
- Cash & Equivalents
- Long-Term Debt

Calculates:

- Net Profit Margin
- Operating Margin
- Return on Assets
- Return on Equity

### RAG Question Answering

Users can upload an annual report and ask questions about it.

The system:

1. Extracts page-aware text from the PDF
2. Splits the report into chunks
3. Generates embeddings
4. Retrieves relevant chunks
5. Sends the retrieved context to an LLM
6. Returns an answer with page citations

## Tech Stack

- Python
- Streamlit
- PyMuPDF
- Sentence Transformers
- NumPy
- Pandas
- Groq
- Google Colab
- GitHub

## Project Structure

investiq/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── src/
│   ├── analytics.py
│   └── rag_pipeline.py
└── data/

## Running the Application

Install dependencies:

    pip install -r requirements.txt

Set the Groq API key:

    export GROQ_API_KEY='your_api_key'

Run Streamlit:

    streamlit run app.py

## Important

Do not commit API keys, uploaded annual reports, or generated financial data to GitHub.

Apple's 2025 annual report was used as a development test document. The application is designed to process uploaded annual reports dynamically.
