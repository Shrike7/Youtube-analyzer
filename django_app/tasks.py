from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models.mongo import File, Video as VideoMongo
from .models.postgres import Category, Chanel, UserProfile, Video as VideoPostgres, WatchRecord
from bson import ObjectId
from .youtube_requests import get_video_category


# TODO: Check for edge cases. Error handling
# TODO: Check for youtube api token run out
# TODO: Check for deleted video
# TODO: Check for youtube music objects
# TODO: Check for advertisement objects
@shared_task
def proceed_video(file_id_str):
    """Proceed not proceeded videos in file.
    Get video category from YouTube api.
    Check if already video, chanel, watch record in postgres db.
    If not: insert.
    Update status of video in mongo db."""
    file_object_id = ObjectId(file_id_str)

    # Find file in mongo
    file = File.objects.filter(id=file_object_id).first()
    if not file:
        # Probably file was deleted before task started
        # TODO: print log message
        return

    user_profile_id = file.user_profile_id

    # Find all videos with host=file_id and status False
    videos = VideoMongo.objects.filter(host=file_object_id, status=False)

    for video in videos:
        # Get id after "?v=", https://www.youtube.com/watch?v=2Vm1VQix4AA
        video_id = video.titleUrl.split("=")[-1]
        # Get id after "channel/", https://www.youtube.com/channel/UCcDj9XqT2YQERsdAnHGR7xg
        chanel_id = video.subtitles[0].url.split('/')[-1]

        videos_pg = VideoPostgres.objects.filter(custom_id=video_id)
        if not videos_pg.exists():
            # Get category id from YouTube api
            video_category_id = get_video_category(video_id)

            if video_category_id is None:
                # Probably Ytb api quota run out
                # Stop task. We will try again later
                return

            if video_category_id == 0:
                print(f"Video not found. Video {video_id} will be deleted from mongo")
                video.delete()
                continue

            category_id = Category.objects.filter(id=video_category_id)
            if not category_id:
                # Yb category is always predefined in db
                # TODO: print log message
                # Almost impossible to get here
                return

            category_id = category_id.first()

            # Check if chanel already in db
            channels_pg = Chanel.objects.filter(custom_id=chanel_id)
            channel_pg = None
            if not channels_pg.exists():
                # Insert chanel in db
                channel_pg = Chanel.objects.create(
                    custom_id=chanel_id,
                    name=video.subtitles[0].name
                )
                channel_pg.save()
            else:
                channel_pg = channels_pg.first()

            # Insert video in db
            video_pg = VideoPostgres.objects.create(
                custom_id=video_id,
                name=video.title,
                chanel=channel_pg,
                category=category_id
            )
            video_pg.save()

        else:
            # Video is already in db.
            # Check if it's same watch record
            video_pg = videos_pg.first()
            watch_records_pg = WatchRecord.objects.filter(
                video=video_id, user_profile_id=user_profile_id, time=video.time
            )
            # Skip if same watch record already in db
            if watch_records_pg.exists():
                # Update status
                video.status = True
                video.save()
                continue

        # Insert watch record
        user_profile = UserProfile.objects.filter(id=user_profile_id).first()
        watch_record_pg = WatchRecord.objects.create(
            time=video.time,
            user_profile=user_profile,
            video=video_pg
        )
        watch_record_pg.save()

        # Update status
        video.status = True
        video.save()

    # Check if there is not proceeded videos in file
    videos = VideoMongo.objects.filter(host=file_object_id, status=False)
    if len(videos) == 0:
        print("All videos proceeded")
        # We finished all not proceeded videos in file
        # Update status of file
        file.status = True
        file.save()
