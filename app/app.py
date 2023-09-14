import json
import psycopg2
import os
from dotenv import load_dotenv

def main():
    load_dotenv()

    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            dbname=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            port=os.environ.get("DB_PORT")
        )

        cursor = conn.cursor()

        with open("../data/watch-history.json") as history:
            data = json.load(history)

            for watch_record in data:
                video_id = watch_record["titleUrl"].split("=")[-1]
                video_name = watch_record["title"]

                chanel_id = watch_record["subtitles"][0]["url"].split('/')[-1]
                chanel_name = watch_record["subtitles"][0]["name"]

                watch_time = watch_record["time"]

                print(video_id, video_name, chanel_id, chanel_name, watch_time)

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