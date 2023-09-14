from youtube_requests import get_video_category


def proceed_record_to_db(cursor, video_id, video_name, chanel_id, chanel_name, watch_time, user_id, api_key):
    # Check if video already in db
    if is_video_in_db(cursor, video_id) is False:
        # Check if chanel in db
        if is_chanel_in_db(cursor, chanel_id) is False:
            # Add chanel in db
            # TODO Some additional check if added
            insert_chanel(cursor, chanel_id, chanel_name)

        # Ask API for video category
        video_category_id = get_video_category(api_key, video_id)

        # Add video in db
        insert_video(cursor, video_id, video_name, chanel_id, video_category_id)

    # Add watch record
    insert_watch_record(cursor, video_id, user_id, watch_time)


def is_video_in_db(cursor, video_id):
    cursor.execute("SELECT * FROM video WHERE id_video = %s", (video_id,))
    return cursor.fetchone() is not None


def is_chanel_in_db(cursor, chanel_id):
    cursor.execute("SELECT * FROM chanel WHERE id_chanel = %s", (chanel_id,))
    return cursor.fetchone() is not None


def insert_chanel(cursor, chanel_id, chanel_name):
    insert_script = "INSERT INTO chanel (id_chanel, name) VALUES (%s, %s)"
    insert_values = (chanel_id, chanel_name)

    cursor.execute(insert_script, insert_values)


def insert_video(cursor, video_id, video_name, chanel_id, category_id):
    insert_script = "INSERT INTO video (id_video, name, id_chanel, id_category) VALUES (%s, %s, %s, %s)"
    insert_values = (video_id, video_name, chanel_id, category_id)

    cursor.execute(insert_script, insert_values)


def insert_watch_record(cursor, video_id, user_id, watch_time):
    insert_script = ("INSERT INTO watchrecord (id_video, id_user, time) "
                     "VALUES (%s, %s, TO_TIMESTAMP(%s, \'YYYY-MM-DDTHH24:MI:SS.MSSTZD\') "
                     "AT TIME ZONE \'UTC\')")
    insert_values = (video_id, user_id, watch_time)

    cursor.execute(insert_script, insert_values)