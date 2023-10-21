from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import File, Video, Subtitle
from bson import ObjectId


@shared_task
def proceed_video(file_id_str):
    file_object_id = ObjectId(file_id_str)

    # Find all videos with host=file_id
    videos = Video.objects.filter(host=file_object_id)

    for video in videos:
        print(video.title)
        print("------------------")

