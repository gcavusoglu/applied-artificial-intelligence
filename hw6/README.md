
- Uses SQLite 3 databases
- Uses "unsloth/gemma-4-12B-it" model
- Main program is in app.py
- Before running app.py, run create-table.py.
- Only actions AI can take is list books and buy books. Buying a book removes it from the DB.
- Examples:

"List me books of AI Book Cafe"

🚀 User Query: List me books of AI Book Cafe
  [Step 1] Calling: 'get_book_list'
  [Step 1] 🔌 Tool Result: [{'id': 1, 'name': 'The Alchemist', 'writer': 'Paulo Coelho', 'genre': 'allegory'}, {'id': 2, 'name': 'Dune', 'writer': 'Frank Herbert', 'genre': 'science fiction'}, {'id': 3, 'name': 'Murder on the Orient Express', 'writer': 'Agatha Christie', 'genre': 'mystery'}, {'id': 4, 'name': 'Sapiens: A Brief History of Humankind', 'writer': 'Yuval Noah Harari', 'genre': 'history'}, {'id': 5, 'name': 'Pride and Prejudice', 'writer': 'Jane Austen', 'genre': 'romance'}, {'id': 6, 'name': 'Atomic Habits', 'writer': 'James Clear', 'genre': 'self-help'}]

📚 AI Book Cafe Catalog

Here is the list of books currently available at the AI Book Cafe:
- The Alchemist
  Author: Paulo Coelho
  Genre: Allegory
- Dune
  Author: Frank Herbert
  Genre: Science Fiction
- Murder on the Orient Express
  Author: Agatha Christie
  Genre: Mystery
- Sapiens: A Brief History of Humankind
  Author: Yuval Noah Harari
  Genre: History
- Pride and Prejudice
  Author: Jane Austen
  Genre: Romance
- Atomic Habits
  Author: James Clear
  Genre: Self-help

"Buy 'Dune' from AI Book Cafe"

🚀 User Query: Buy 'Dune' from AI Book Cafe
  [Step 1] Calling: 'buy_book'
  [Step 1] 🔌 Tool Result: Successfully bought book "Dune"
Successfully bought book "Dune"