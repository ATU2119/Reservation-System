import sqlite3
import unittest

def create_database():
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    # Create Items table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        availability BOOLEAN NOT NULL DEFAULT TRUE
    );
    ''')

    # Create Reservations table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users (id),
        FOREIGN KEY (item_id) REFERENCES Items (id)
    );
    ''')

    conn.commit()
    conn.close()
    print("Database and tables created")

# Call the function to create the database and tables
create_database()

def add_user(username, email, password_hash):
    """
    Adds a new user to the Users table.
    
    Args:
    username (str): The username of the user.
    email (str): The email address of the user.
    password_hash (str): The hashed password of the user.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('reservations.db')
        cursor = conn.cursor()
        
        # SQL query to insert a new user
        sql = "INSERT INTO Users (username, email, password_hash) VALUES (?, ?, ?)"
        
        # Execute the SQL statement
        cursor.execute(sql, (username, email, password_hash))
        
        # Commit the changes
        conn.commit()
        print("User added successfully: {}".format(username))
    
    except sqlite3.IntegrityError as e:
        print("Error adding user: ", e)
    
    finally:
        # Close the connection to the database
        conn.close()

# Example usage:
add_user('jane_doe', 'jane@example.com', 'secure_hashed_password')

def add_item(name, description, availability=True):
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Items (name, description, availability) VALUES (?, ?, ?)", (name, description, availability))
    conn.commit()
    conn.close()

def make_reservation(user_id, item_id, start_date, end_date):
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Reservations (user_id, item_id, start_date, end_date) VALUES (?, ?, ?, ?)",
                   (user_id, item_id, start_date, end_date))
    conn.commit()
    conn.close()

def fetch_reservations():
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Reservations")
    rows = cursor.fetchall()
    conn.close()
    return rows

def setup_test_data():
    # Add users
    add_user('alice', 'alice@example.com', 'hashed_password_123')
    add_user('bob', 'bob@example.com', 'hashed_password_abc')
    
    # Add items
    add_item('Conference Room A', 'A large room for meetings', True)
    add_item('Banquet Hall', 'Spacious hall for events', True)
    
    # Make reservations
    make_reservation(1, 1, '2024-06-01', '2024-06-02')
    make_reservation(2, 2, '2024-06-15', '2024-06-16')

# Assuming all function definitions are in place, call the setup:
setup_test_data()

def test_user_creation():
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username='alice'")
    result = cursor.fetchone()
    assert result is not None, "Test failed: User 'alice' was not found in the database."
    print("Test passed: User 'alice' found.")

def test_item_creation():
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Items WHERE name='Conference Room A'")
    result = cursor.fetchone()
    assert result is not None, "Test failed: Item 'Conference Room A' was not found."
    print("Test passed: Item 'Conference Room A' found.")

def test_reservation_creation():
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Reservations WHERE user_id=1")
    result = cursor.fetchall()
    assert len(result) > 0, "Test failed: No reservations found for user_id 1."
    print("Test passed: Reservation found for user_id 1.")

# Run tests
test_user_creation()
test_item_creation()
test_reservation_creation()

class ReservationSystemTest(unittest.TestCase):
    def test_user_creation(self):
        # similar test logic
        pass
    
    def test_item_creation(self):
        # similar test logic
        pass
    
    def test_reservation_creation(self):
        # similar test logic
        pass

if __name__ == '__main__':
    unittest.main()
