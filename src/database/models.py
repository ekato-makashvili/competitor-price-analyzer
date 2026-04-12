import psycopg2
import os

def get_connection():
    """
    Establish a secure connection to the PostgreSQL database.
    Configuration is pulled directly from environment variables 
    to ensure security and prevent sensitive data leakage.
    """
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def init_db():
    """Initializes the database by creating the prices table if it doesn't exist."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS prices (
                id SERIAL PRIMARY KEY,
                product_name TEXT NOT NULL,
                price INTEGER NOT NULL,
                currency TEXT DEFAULT 'GEL',
                store_name TEXT NOT NULL,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT unique_product_price_store UNIQUE (product_name, price, store_name)
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Database initialized successfully.")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")

def save_price(product_name, price, currency="GEL", store_name="Zoommer"):
    """Saves a single product record to the database."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO prices (product_name, price, currency, store_name) 
               VALUES (%s, %s, %s, %s)
               ON CONFLICT (product_name, price, store_name) DO NOTHING""", 
            (product_name, price, currency, store_name)
        )
        conn.commit()
        cur.close()
        conn.close()
        print(f"💾 Saved: [{store_name}] {product_name}")
    except Exception as e:
        print(f"❌ DB Error saving {product_name}: {e}")