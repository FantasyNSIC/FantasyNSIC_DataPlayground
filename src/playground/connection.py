import psycopg2

def connect_to_fantasyDB():
    
    # Read database credentials from file
    with open('src/playground/dbcreds.txt', 'r') as creds:
        host = creds.readline().strip().replace('host=', '')
        port = creds.readline().strip().replace('port=', '')
        database = creds.readline().strip().replace('database=', '')
        user = creds.readline().strip().replace('username=', '')
        password = creds.readline().strip().replace('password=', '')

    print("Connecting to database...")

    # Initialize connection and cursor
    conn = None

    try:
        # Connect to database
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        print("Connected!")

        # Return connection
        return conn

    except Exception as e:
        print(f"Error: {e}")
        if conn is not None:
            conn.close()
