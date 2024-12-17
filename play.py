import sqlite3

def initialize_database():
    """Initialize the SQLite database."""
    conn = sqlite3.connect('rental_booking_system.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS rentals (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT,
                        price_per_month REAL NOT NULL,
                        is_available BOOLEAN NOT NULL DEFAULT 1)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        rental_id INTEGER NOT NULL,
                        booking_date TEXT NOT NULL,
                        FOREIGN KEY(user_id) REFERENCES users(id),
                        FOREIGN KEY(rental_id) REFERENCES rentals(id))''')

    conn.commit()
    conn.close()

def register_user(name, email, password):
    """Register a new user."""
    conn = sqlite3.connect('rental_booking_system.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
        conn.commit()
        print("User registered successfully!")
    except sqlite3.IntegrityError:
        print("Error: Email already exists.")
    conn.close()

def list_rentals():
    """List all available rentals."""
    conn = sqlite3.connect('rental_booking_system.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, description, price_per_month FROM rentals WHERE is_available = 1')
    rentals = cursor.fetchall()
    conn.close()

    if rentals:
        print("Available Rentals:")
        for rental in rentals:
            print(f"ID: {rental[0]}, Title: {rental[1]}, Description: {rental[2]}, Price: {rental[3]} RWF/month")
    else:
        print("No rentals available.")

def book_rental(user_id, rental_id):
    """Book a rental for a user."""
    conn = sqlite3.connect('rental_booking_system.db')
    cursor = conn.cursor()
    try:
        # Check if the rental is available
        cursor.execute('SELECT is_available FROM rentals WHERE id = ?', (rental_id,))
        rental = cursor.fetchone()
        if rental and rental[0]:
            # Book the rental
            cursor.execute('INSERT INTO bookings (user_id, rental_id, booking_date) VALUES (?, ?, date("now"))', (user_id, rental_id))
            cursor.execute('UPDATE rentals SET is_available = 0 WHERE id = ?', (rental_id,))
            conn.commit()
            print("Rental booked successfully!")
        else:
            print("Error: Rental is not available.")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    conn.close()

# Example usage
if __name__ == "__main__":
    initialize_database()

    print("Welcome to the Online Rental Booking System!")

    while True:
        print("\nMenu:")
        print("1. Register")
        print("2. List Rentals")
        print("3. Book Rental")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            register_user(name, email, password)

        elif choice == "2":
            list_rentals()

        elif choice == "3":
            user_id = int(input("Enter your user ID: "))
            rental_id = int(input("Enter the rental ID you want to book: "))
            book_rental(user_id, rental_id)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid Please try again.")
