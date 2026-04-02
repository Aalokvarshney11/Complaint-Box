import hashlib
from database import get_connection, create_tables

# Pehle tables banao
create_tables()

# Manager details
username = "aalok"
password = "12345678"

# Password hash karo
hashed_password = hashlib.sha256(password.encode()).hexdigest()

# DB mein insert karo
conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
    INSERT INTO managers (username, password) 
    VALUES (?,?)
""", (username, hashed_password))

conn.commit()
conn.close()

print("Manager account ban gaya!")