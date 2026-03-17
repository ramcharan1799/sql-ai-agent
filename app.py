import streamlit as st
import pandas as pd
from utils.db import get_schema, run_query, sample_data
from utils.agent import generate_sql, generate_summary

st.set_page_config(page_title="SQL AI Agent", page_icon="🗄️", layout="wide")

st.title("🗄️ SQL AI Agent")
st.caption("Ask questions about the company database in plain English.")

# Load schema once into session
if "schema" not in st.session_state:
    st.session_state.schema = get_schema()

# ── Sidebar — schema explorer ─────────────────────────────────────────────────
with st.sidebar:
    st.header("Database Schema")
    st.code(st.session_state.schema, language="sql")
    st.divider()

    if st.button("Show sample data"):
        samples = sample_data()
        for table, data in samples.items():
            st.subheader(table)
            st.text(data)

    st.divider()
    st.caption("Built with OpenAI + SQLite + Streamlit")

# ── Suggested questions ───────────────────────────────────────────────────────
st.subheader("Try asking:")
suggestions = [
    "Show me the top 5 highest paid employees",
    "How many employees are in each department?",
    "What is the total sales amount by region?",
    "List all AI Engineers with their salaries",
    "Which product had the highest total sales?",
    "Show employees hired in the last 6 months",
]
cols = st.columns(3)
for i, s in enumerate(suggestions):
    if cols[i % 3].button(s, use_container_width=True):
        st.session_state.question = s

# ── Chat history ──────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

for entry in st.session_state.history:
    with st.expander(f"Q: {entry['question']}", expanded=False):
        st.code(entry["sql"], language="sql")
        if entry["error"]:
            st.error(entry["error"])
        else:
            st.info(entry["summary"])
            st.dataframe(entry["df"], use_container_width=True)

# ── Input ─────────────────────────────────────────────────────────────────────
st.divider()
question = st.text_input(
    "Ask a question:",
    value=st.session_state.get("question", ""),
    placeholder="e.g. What is the average salary by department?",
    key="input_box"
)

if st.button("Run", type="primary") and question.strip():
    st.session_state.question = ""
    with st.spinner("Generating SQL and running query..."):
        sql = generate_sql(question, st.session_state.schema)
        df, error = run_query(sql)

        if error:
            summary = ""
        else:
            preview = df.head(5).to_string(index=False) if not df.empty else "No results"
            summary = generate_summary(question, sql, preview)

        entry = {
            "question": question,
            "sql": sql,
            "df": df,
            "error": error,
            "summary": summary
        }
        st.session_state.history.insert(0, entry)

    st.subheader("Generated SQL")
    st.code(sql, language="sql")

    if error:
        st.error(f"Query error: {error}")
    else:
        st.info(summary)
        st.subheader(f"Results — {len(df)} rows")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False)
        st.download_button("Download CSV", csv, "results.csv", "text/csv")
