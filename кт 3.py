import csv

def get_books(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='|')
        rows = list(reader)[1:]
        return [
            [isbn, title, author, int(quantity), float(price)]
            for isbn, title, author, quantity, price in rows
        ]
        
books = get_books("books.csv")
print(books)

def filtered_books(books, keyword):
    return [
        [isbn, f"{title}, {author}", quantity, price]
        for isbn, title, author, quantity, price in books
        if keyword.lower() in title.lower()
    ]
    
books = get_books("books.csv")
python_books = filtered_books(books, "python")
print(python_books)

def calculate_total_prices(books):
    return [
        (book[0], book[-2] * book[-1])
        for book in books
    ]
books = get_books("books.csv") 
filtered = filtered_books(books, "python")
totals_original = calculate_total_prices(books)
totals_filtered = calculate_total_prices(filtered)

print("Для исходного списка:", totals_original)
print("Для отфильтрованного списка:", totals_filtered)
