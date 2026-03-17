# SQL AI Agent

A natural language interface over a SQL database. Ask questions in plain English, get back SQL queries and results instantly.

## How it works

1. User types a question in plain English
2. GPT-3.5 reads the database schema and generates a valid SQLite SELECT query
3. The query runs against a local SQLite database (read-only, injection-safe)
4. Results are returned as a table with an AI-generated plain English summary
5. Results can be downloaded as CSV

## Database

3 tables, ~600 rows of realistic Indian company data:
- `departments` — 5 departments (Engineering, Sales, HR, Marketing, Data & AI)
- `employees` — 100 employees with roles, salaries, cities, hire dates
- `sales` — 500 sales transactions with products, amounts, regions, status

## Tech stack

- **OpenAI GPT-3.5** — natural language to SQL conversion
- **SQLite** — lightweight embedded database
- **pandas** — query result handling
- **Streamlit** — interactive UI with query history and CSV export
- **python-dotenv** — API key management

## Project structure
```
sql-ai-agent/
├── app.py              # Streamlit UI
├── create_db.py        # Database setup script
├── company.db          # SQLite database (auto-generated)
├── utils/
│   ├── db.py           # Schema reader, query runner, safety guard
│   └── agent.py        # GPT prompt, SQL generation, summary
└── requirements.txt
```

## Run locally
```
git clone https://github.com/ramcharan1799/sql-ai-agent
cd sql-ai-agent
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
echo "OPENAI_API_KEY=your-key-here" > .env
python create_db.py
streamlit run app.py
```

## Sample questions to try

- "Show me the top 5 highest paid employees"
- "What is the total sales amount by region?"
- "List all AI Engineers with their salaries"
- "How many employees are in each department?"
- "Which product had the highest total sales?"

## What I learned

- How to make GPT generate valid SQL using schema-aware prompting
- How to safely execute LLM-generated SQL (read-only guard, forbidden keyword check)
- How to combine LLM output with a real database query pipeline
- Session state management and query history in Streamlit

## Author

Built as part of my AI Engineer learning journey — roadmap.sh/ai-engineer
