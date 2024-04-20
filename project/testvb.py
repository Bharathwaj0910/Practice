import sqlite3

    # Connect to the database
conn = sqlite3.connect('users_credentials.db')
cursor = conn.cursor()

    # Execute a DELETE statement to remove the last two records

    # Execute a SELECT statement to retrieve data from the users table
#cursor.execute("UPDATE users SET notify = ? WHERE email = ?", ( True , "bharathwaj0910@gmail.com"))
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
for user in users:
    print(users)

    # Commit the transaction
conn.commit()

    # Close the connection
conn.close()