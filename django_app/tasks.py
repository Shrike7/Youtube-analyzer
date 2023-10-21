from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models.mongo import File, Video as VideoMongo, Subtitle
from .models.postgres import Category, Chanel, UserProfile, Video as VideoPostgres, WatchRecord
from bson import ObjectId


@shared_task
def proceed_video(file_id_str):
    file_object_id = ObjectId(file_id_str)

    # Find all videos with host=file_id and status False
    videos = VideoMongo.objects.filter(host=file_object_id, status=False)

    for video in videos:
        print(video.title)
        print("------------------")

