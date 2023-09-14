import psycopg2
import os
from dotenv import load_dotenv

def main():
    load_dotenv()

    conn = None
    cursor = None

    create_script_path = "../db/create_script.sql"
    insert_script_path = "../db/insert_script.sql"

    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            dbname=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            port=os.environ.get("DB_PORT")
        )

        cursor = conn.cursor()

        with open(create_script_path, 'r') as create_script_file:
            create_script_sql = create_script_file.read()

        cursor.execute(create_script_sql)

        with open(insert_script_path, 'r') as insert_script_file:
            insert_script_sql = insert_script_file.read()

        cursor.execute(insert_script_sql)

        conn.commit()

    except Exception as error:
        print(error)
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    main()