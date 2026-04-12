# 📊 Competitor Price Analyzer

Automated web scraper (Zoommer.ge) and Streamlit dashboard for price tracking.

## 🛠 Tech Stack
Python (Playwright, SQLAlchemy), PostgreSQL, Streamlit, Docker.

## 🚀 Quick Start

1. **Clone & Navigate:**
   ```bash
   git clone [https://github.com/ekato-makashvili/competitor-price-analyzer.git](https://github.com/ekato-makashvili/competitor-price-analyzer.git)
   cd competitor-price-analyzer
Configure Variables:
Create a .env file in the root directory:

Code snippet
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=price_analyzer
DB_HOST=db
DB_PORT=5432
Launch with Docker:

Bash
docker-compose up --build
🔗 Access
Dashboard: http://localhost:8501

Database: localhost:5432

🧹 Data Cleanup (SQL)
To remove duplicates:

SQL
DELETE FROM prices a USING prices b 
WHERE a.id < b.id AND a.product_name = b.product_name 
AND a.price = b.price AND a.store_name = b.store_name;
Developed for price monitoring and analysis.
