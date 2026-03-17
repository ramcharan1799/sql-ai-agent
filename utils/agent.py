import os
import re
from openai import OpenAI
from dotenv import load_dotenv
from utils.db import get_schema

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are an expert SQL assistant. You help users query a SQLite company database.

Given the database schema below, convert the user's natural language question into a valid SQLite SELECT query.

Rules:
- Return ONLY the raw SQL query, nothing else
- No markdown, no code blocks, no backticks, no explanation
- Only use SELECT statements
- Use proper SQLite syntax
- Use table aliases for readability
- Always use LIMIT 100 unless the user asks for all records
- For salary/amount columns, round to 2 decimal places
- Use strftime for date operations in SQLite

Schema:
{schema}
"""

def generate_sql(question: str, schema: str) -> str:
    """Converts a natural language question to a SQL query."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.format(schema=schema)},
            {"role": "user", "content": question}
        ],
        temperature=0,
        max_tokens=300
    )
    sql = response.choices[0].message.content.strip()
    sql = re.sub(r"```(?:sql)?", "", sql).replace("```", "").strip()
    return sql


def generate_summary(question: str, sql: str, result_preview: str) -> str:
    """Generates a plain English summary of the query results."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful data analyst. Summarise query results in 2-3 clear sentences. Be specific with numbers."},
            {"role": "user", "content": f"Question: {question}\nSQL: {sql}\nResults preview:\n{result_preview}"}
        ],
        temperature=0.3,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()
