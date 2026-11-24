import json
import sqlite3

with open("catalog.json", "r", encoding="utf-8") as file:
    items = json.load(file)

conn = sqlite3.connect("database.db")
conn.execute("PRAGMA foreign_keys = ON")

with conn:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        );
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            price REAL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES category (id)
        );
        DELETE FROM product;
        DELETE FROM category;
    """)

ids = {}
for item in items:
    name = item["category"]["name"]
    if name not in ids:
        cursor = conn.execute(
            "INSERT INTO category (name, description) VALUES (?, ?)",
            (name, item["category"]["description"]),
        )
        ids[name] = cursor.lastrowid
    conn.execute(
        "INSERT INTO product (product_name, price, category_id) VALUES (?, ?, ?)",
        (item["product_name"], item["price"], ids[name]),
    )

conn.commit()
conn.close()    