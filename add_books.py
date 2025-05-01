import json

# List of books to add
books_to_add = [
    {
        "title": "Seerat-e-Mustafa ﷺ",
        "author": "Maulana Abdul Mustafa A'zami",
        "year": 2020,
        "genre": "Islamic Biography",
        "read": False,
        "description": "Rasoolullah ﷺ ki zindagi ke mukammal pehluon par tahqiqi aur ilm se bharpur kitaab."
    },
    {
        "title": "Ghaus-e-Azam ka Ishq-e-Rasool ﷺ",
        "author": "Allama Abul Hafs Sayyid Muhammad Uwais Qadri",
        "year": 2020,
        "genre": "Islamic Spirituality",
        "read": False,
        "description": "Hazrat Abdul Qadir Jilani رحمۃ اللہ علیہ ka Rasool ﷺ se muhabbat ka roohani izhar."
    },
    {
        "title": "Faizan-e-Khalilullah (Hazrat Ibrahim علیہ السلام)",
        "author": "Mufti Abu Muhammad Aslam Raza Attari",
        "year": 2020,
        "genre": "Islamic Biography",
        "read": False,
        "description": "Seerat-e-Ibrahimi aur unki duaaon ka ilm se bharpur zikr."
    },
    {
        "title": "Faizan-e-Hazrat Khadija tul Kubra رضی اللہ عنہا",
        "author": "Maulana Abu Majid Muhammad Shahid Attari",
        "year": 2020,
        "genre": "Islamic Biography",
        "read": False,
        "description": "Ummahat-ul-Momineen mein sab se pehli, Hazrat Khadija رضی اللہ عنہا ki zindagi aur Rasool ﷺ ke sath unka aham kirdar."
    },
]

# Load existing books if any
try:
    with open("library.json", "r", encoding='utf-8') as f:
        existing_books = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    existing_books = []

# Add new books if they don't already exist
for new_book in books_to_add:
    if not any(book["title"] == new_book["title"] for book in existing_books):
        existing_books.append(new_book)

# Save updated library
with open("library.json", "w", encoding='utf-8') as f:
    json.dump(existing_books, f, indent=4, ensure_ascii=False)

print("Books have been added to the library successfully!") 