import sqlite3
import random
from datetime import datetime, timedelta

random.seed(42)

conn = sqlite3.connect("company.db")
cur = conn.cursor()

# ── Tables ────────────────────────────────────────────────────────────────────
cur.executescript("""
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS sales;

CREATE TABLE departments (
    dept_id   INTEGER PRIMARY KEY,
    dept_name TEXT NOT NULL,
    location  TEXT NOT NULL,
    budget    REAL NOT NULL
);

CREATE TABLE employees (
    emp_id      INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    dept_id     INTEGER REFERENCES departments(dept_id),
    role        TEXT NOT NULL,
    salary      REAL NOT NULL,
    hire_date   TEXT NOT NULL,
    city        TEXT NOT NULL,
    is_active   INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE sales (
    sale_id    INTEGER PRIMARY KEY,
    emp_id     INTEGER REFERENCES employees(emp_id),
    product    TEXT NOT NULL,
    amount     REAL NOT NULL,
    sale_date  TEXT NOT NULL,
    region     TEXT NOT NULL,
    status     TEXT NOT NULL
);
""")

# ── Departments ───────────────────────────────────────────────────────────────
departments = [
    (1, "Engineering",  "Bangalore", 5000000),
    (2, "Sales",        "Mumbai",    3000000),
    (3, "HR",           "Hyderabad", 1500000),
    (4, "Marketing",    "Pune",      2000000),
    (5, "Data & AI",    "Bangalore", 4000000),
]
cur.executemany("INSERT INTO departments VALUES (?,?,?,?)", departments)

# ── Employees ─────────────────────────────────────────────────────────────────
first = ["Aarav","Priya","Rahul","Sneha","Vikram","Ananya","Karthik","Deepa",
         "Rohan","Meera","Arjun","Lakshmi","Aditya","Pooja","Suresh","Kavya",
         "Nikhil","Divya","Sanjay","Nisha","Rajesh","Sunita","Amit","Priyanka",
         "Varun","Shreya","Manish","Ritika","Gaurav","Swathi"]
last  = ["Sharma","Patel","Iyer","Reddy","Singh","Nair","Kumar","Gupta",
         "Rao","Joshi","Mehta","Pillai","Verma","Chopra","Mishra","Bose",
         "Agarwal","Das","Shah","Pandey","Nair","Desai","Jain","Malhotra",
         "Sinha","Chatterjee","Kapoor","Saxena","Tiwari","Menon"]
roles = {1: ["Software Engineer","Senior Engineer","Tech Lead","DevOps Engineer"],
         2: ["Sales Executive","Account Manager","Sales Manager","BDM"],
         3: ["HR Executive","HR Manager","Recruiter","HR Business Partner"],
         4: ["Marketing Executive","Content Strategist","Growth Manager","Brand Manager"],
         5: ["Data Engineer","ML Engineer","AI Engineer","Data Analyst"]}
cities = ["Bangalore","Mumbai","Hyderabad","Pune","Chennai","Delhi","Kolkata","Ahmedabad"]

employees = []
for i in range(1, 101):
    dept_id   = random.randint(1, 5)
    role      = random.choice(roles[dept_id])
    base      = {"Software Engineer":800000,"Senior Engineer":1200000,
                 "Tech Lead":1600000,"DevOps Engineer":900000,
                 "Sales Executive":600000,"Account Manager":900000,
                 "Sales Manager":1300000,"BDM":1000000,
                 "HR Executive":550000,"HR Manager":950000,
                 "Recruiter":600000,"HR Business Partner":850000,
                 "Marketing Executive":650000,"Content Strategist":700000,
                 "Growth Manager":1100000,"Brand Manager":1000000,
                 "Data Engineer":1000000,"ML Engineer":1300000,
                 "AI Engineer":1500000,"Data Analyst":750000}
    salary    = base[role] + random.randint(-50000, 150000)
    days_ago  = random.randint(30, 1800)
    hire_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    city      = random.choice(cities)
    is_active = 1 if random.random() > 0.1 else 0
    name      = f"{random.choice(first)} {random.choice(last)}"
    employees.append((i, name, dept_id, role, salary, hire_date, city, is_active))

cur.executemany("INSERT INTO employees VALUES (?,?,?,?,?,?,?,?)", employees)

# ── Sales ─────────────────────────────────────────────────────────────────────
products = ["DataSync Pro","CloudBase","AI Insights","AutoReport","DataVault",
            "PredictIQ","StreamFlow","QueryMaster","MLPipeline","InsightBoard"]
regions  = ["North","South","East","West","Central"]
statuses = ["Completed","Pending","Cancelled"]
sales_emps = [e[0] for e in employees if e[3] in
              ["Sales Executive","Account Manager","Sales Manager","BDM"]]

sales = []
for i in range(1, 501):
    emp_id    = random.choice(sales_emps)
    product   = random.choice(products)
    amount    = round(random.uniform(10000, 500000), 2)
    days_ago  = random.randint(1, 365)
    sale_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    region    = random.choice(regions)
    status    = random.choices(statuses, weights=[70,20,10])[0]
    sales.append((i, emp_id, product, amount, sale_date, region, status))

cur.executemany("INSERT INTO sales VALUES (?,?,?,?,?,?,?)", sales)

conn.commit()
conn.close()
print("Database created: company.db")
print("  departments: 5 rows")
print("  employees:   100 rows")
print("  sales:       500 rows")
