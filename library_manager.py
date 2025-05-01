import json
import os

class LibraryManager:
    def __init__(self):
        self.books = []
        self.load_library()

    def load_library(self):
        """Load the library from a JSON file if it exists."""
        if os.path.exists("library.json"):
            try:
                with open("library.json", "r") as f:
                    self.books = json.load(f)
            except json.JSONDecodeError:
                print("Error: Invalid library file. Starting with empty library.")
                self.books = []
        else:
            self.books = []

    def save_library(self):
        """Save the library to a JSON file."""
        with open("library.json", "w") as f:
            json.dump(self.books, f, indent=4)

    def add_book(self):
        """Add a new book to the library."""
        print("\n=== Add a New Book ===")
        title = input("Enter the book title: ").strip()
        author = input("Enter the author: ").strip()
        
        while True:
            try:
                year = int(input("Enter the publication year: "))
                if year < 0 or year > 2100:
                    print("Please enter a valid year between 0 and 2100.")
                    continue
                break
            except ValueError:
                print("Please enter a valid year (numbers only).")

        genre = input("Enter the genre: ").strip()
        
        while True:
            read_status = input("Have you read this book? (yes/no): ").lower()
            if read_status in ["yes", "no"]:
                break
            print("Please enter 'yes' or 'no'.")

        book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": read_status == "yes"
        }
        
        self.books.append(book)
        self.save_library()
        print("Book added successfully!")

    def remove_book(self):
        """Remove a book from the library."""
        print("\n=== Remove a Book ===")
        title = input("Enter the title of the book to remove: ").strip()
        
        found_books = [book for book in self.books if book["title"].lower() == title.lower()]
        
        if not found_books:
            print("Book not found in the library.")
            return
        
        if len(found_books) > 1:
            print("\nMultiple books found with that title:")
            for i, book in enumerate(found_books, 1):
                print(f"{i}. {book['title']} by {book['author']} ({book['year']})")
            
            while True:
                try:
                    choice = int(input("\nEnter the number of the book to remove: "))
                    if 1 <= choice <= len(found_books):
                        book_to_remove = found_books[choice - 1]
                        self.books.remove(book_to_remove)
                        self.save_library()
                        print("Book removed successfully!")
                        return
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
        else:
            self.books.remove(found_books[0])
            self.save_library()
            print("Book removed successfully!")

    def search_books(self):
        """Search for books by title or author."""
        print("\n=== Search for a Book ===")
        print("Search by:")
        print("1. Title")
        print("2. Author")
        
        while True:
            try:
                choice = int(input("Enter your choice: "))
                if choice in [1, 2]:
                    break
                print("Please enter 1 or 2.")
            except ValueError:
                print("Please enter a valid number.")

        search_term = input("Enter the search term: ").strip().lower()
        
        if choice == 1:
            results = [book for book in self.books if search_term in book["title"].lower()]
        else:
            results = [book for book in self.books if search_term in book["author"].lower()]

        if not results:
            print("No matching books found.")
            return

        print("\nMatching Books:")
        for i, book in enumerate(results, 1):
            read_status = "Read" if book["read"] else "Unread"
            print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")

    def display_all_books(self):
        """Display all books in the library."""
        if not self.books:
            print("\nYour library is empty.")
            return

        print("\n=== Your Library ===")
        for i, book in enumerate(self.books, 1):
            read_status = "Read" if book["read"] else "Unread"
            print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")

    def display_statistics(self):
        """Display library statistics."""
        total_books = len(self.books)
        if total_books == 0:
            print("\nNo books in the library.")
            return

        read_books = sum(1 for book in self.books if book["read"])
        percentage_read = (read_books / total_books) * 100

        print("\n=== Library Statistics ===")
        print(f"Total books: {total_books}")
        print(f"Percentage read: {percentage_read:.1f}%")

def main():
    library = LibraryManager()
    
    while True:
        print("\n=== Personal Library Manager ===")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search for a book")
        print("4. Display all books")
        print("5. Display statistics")
        print("6. Exit")
        
        try:
            choice = int(input("\nEnter your choice: "))
            
            if choice == 1:
                library.add_book()
            elif choice == 2:
                library.remove_book()
            elif choice == 3:
                library.search_books()
            elif choice == 4:
                library.display_all_books()
            elif choice == 5:
                library.display_statistics()
            elif choice == 6:
                print("\nLibrary saved to file. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    main() 