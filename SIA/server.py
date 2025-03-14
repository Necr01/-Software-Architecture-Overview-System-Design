import sqlite3
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer

DB_FILE = "database/library.db"

# Initialize the database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        category TEXT,
        status TEXT
    )
    """)

    # Insert sample books if the table is empty
    cursor.execute("SELECT COUNT(*) FROM books")
    if cursor.fetchone()[0] == 0:
        books = [
            ("To Kill a Mockingbird", "Harper Lee", "Fiction", "Available"),
            ("1984", "George Orwell", "Fiction", "Available"),
            ("The Great Gatsby", "F. Scott Fitzgerald", "Fiction", "Available"),
            ("Moby-Dick", "Herman Melville", "Adventure", "Available"),
            ("The Odyssey", "Homer", "Epic", "Available"),
            ("Crime and Punishment", "Fyodor Dostoevsky", "Philosophy", "Available")
            
        ]
        cursor.executemany("INSERT INTO books (title, author, category, status) VALUES (?, ?, ?, ?)", books)
    
    conn.commit()
    conn.close()

# Custom HTTP request handler
class LibraryHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/books":
            self.get_books()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/borrow":
            self.update_book_status("Borrowed")
        elif self.path == "/return":
            self.update_book_status("Available")
        else:
            super().do_GET()

    def get_books(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        books = [{"id": row[0], "title": row[1], "author": row[2], "category": row[3], "status": row[4]} for row in cursor.fetchall()]
        conn.close()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(books).encode())

    def update_book_status(self, status):
        content_length = int(self.headers["Content-Length"])
        post_data = json.loads(self.rfile.read(content_length).decode())
        book_id = post_data.get("id")

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("UPDATE books SET status = ? WHERE id = ?", (status, book_id))
        conn.commit()
        conn.close()

        self.send_response(200)
        self.end_headers()

# Run the server
if __name__ == "__main__":
    init_db()
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, LibraryHandler)
    print("Server running at http://localhost:8000")
    httpd.serve_forever()
