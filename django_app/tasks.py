from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models.mongo import File, Video as VideoMongo, Subtitle
from .models.postgres import Category, Chanel, UserProfile, Video as VideoPostgres, WatchRecord
from bson import ObjectId
from .youtube_requests import get_video_category


# TODO: Check for edge cases. Error handling
@shared_task
def proceed_video(file_id_str):
    file_object_id = ObjectId(file_id_str)

    # Find all videos with host=file_id and status False
    videos = VideoMongo.objects.filter(host=file_object_id, status=False)

    for video in videos:
        video_id = video.titleUrl.split("=")[-1]
        chanel_id = video.subtitles[0].url.split('/')[-1]

        videos_pg = VideoPostgres.objects.filter(custom_id=video_id)
        if not videos_pg.exists():
            # Check if chanel already in db
            chanels_pg = Chanel.objects.filter(custom_id=chanel_id)
            chanel_pg = None
            if not chanels_pg.exists():
                # Insert chanel in db
                chanel_pg = Chanel.objects.create(
                    custom_id=chanel_id,
                    name=video.subtitles[0].name
                )
                chanel_pg.save()
            else:
                chanel_pg = chanels_pg.first()

            video_category_id = get_video_category(video_id)
            category_id = Category.objects.filter(custom_id=video_category_id).first()

            # Insert video in db
            video_pg = VideoPostgres.objects.create(
                custom_id=video_id,
                name=video.title,
                chanel=chanel_pg,
                category=category_id
            )

            video_pg.save()

            # Insert watch record
            user_profile = UserProfile.objects.filter(id=video.user).first()
            watch_record_pg = WatchRecord.objects.create(
                time=video.time,
                user_profile=user_profile,
                video=video_pg
            )

            watch_record_pg.save()

            # Update status
            video.status = True
            video.save()
        else:
            # Video is already in db. Check if its same watch record
            video_pg = videos_pg.first()
            watch_records_pg = WatchRecord.objects.filter(video=video_id, user_profile_id=video.user, time=video.time)
            if not watch_records_pg.exists():
                # Insert watch record
                user_profile = UserProfile.objects.filter(id=video.user).first()
                watch_record_pg = WatchRecord.objects.create(
                    time=video.time,
                    user_profile=user_profile,
                    video=video_pg
                )

                watch_record_pg.save()

                # Update status
                video.status = True
                video.save()
            else:
                # Watch record already in db
                pass
            pass


# {
#   "header": "YouTube",
#   "title": "Watched Dad Jokes | Don\u0027t laugh Challenge | Best Moments 2 | Raise Your Spirits",
#   "titleUrl": "https://www.youtube.com/watch?v\u003d2Vm1VQix4AA",
#   "subtitles": [{
#     "name": "YeahMad",
#     "url": "https://www.youtube.com/channel/UCcDj9XqT2YQERsdAnHGR7xg"
#   }],
#   "time": "2023-08-15T08:49:17.849Z",
#   "products": ["YouTube"],
#   "activityControls": ["YouTube watch history"]
# }