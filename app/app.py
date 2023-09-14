import json

with open("../data/watch-history.json") as history:
    data = json.load(history)

    for watch_record in data:
        video_id = watch_record["titleUrl"].split("=")[-1]
        video_name = watch_record["title"]

        chanel_id = watch_record["subtitles"][0]["url"].split('/')[-1]
        chanel_name = watch_record["subtitles"][0]["name"]

        watch_time = watch_record["time"]

        print(video_id, video_name, chanel_id, chanel_name, watch_time)