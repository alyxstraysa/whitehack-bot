import psycopg2
from secrets import USER, PASSWORD, DATABASE, DATABASE_URL

try:
    conn = psycopg2.connect(DATABASE_URL, sslmode='require',
                        database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    
    cursor.execute(
        """
        DROP TABLE IF EXISTS elo_tracker;

        CREATE TABLE elo_tracker (
            discord_id INT PRIMARY KEY,
            division VARCHAR(50),
            LP integer
        );
        """
    )

    cursor.execute(
        """
        INSERT INTO elo_tracker VALUES (
            123, 'Iron', 20
        );    
        """
    )

    cursor.execute(
        """
        SELECT * FROM elo_tracker;
        """
    )
    
    record = cursor.fetchall()
    print(record)

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database conn.
        if(conn):
            cursor.close()
            conn.close()
            print("PostgreSQL conn is closed")
