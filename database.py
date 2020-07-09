import psycopg2
from secrets import USER, PASSWORD, DATABASE, DATABASE_URL

def create_table():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require',
                            database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    cursor.execute(
            """
            DROP TABLE IF EXISTS elo_tracker;

            CREATE TABLE elo_tracker (
                discord_id VARCHAR(50) PRIMARY KEY,
                division VARCHAR(50),
                LP integer
            );
            """
    )
    conn.commit()
    
    conn.close()
    

def matchmaking(user):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require',
                            database=DATABASE, user=USER, password=PASSWORD)
        cursor = conn.cursor()
        
        data = (user,)
        cursor.execute(
            """
            INSERT INTO elo_tracker (discord_id, division, LP)
            VALUES
                (
                    %s,
                    'Iron 1',
                    0
                ) 
            ON CONFLICT (discord_id) 
            DO NOTHING;
            """,
            data
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
                conn.commit()
                cursor.close()
                conn.close()
                print("PostgreSQL conn is closed")
