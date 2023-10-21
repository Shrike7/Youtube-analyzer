from django.shortcuts import render, HttpResponse
from .forms import JSONUploadForm
import json
from .models import File, Video, Subtitle
from .tasks import proceed_video


def home(request):
    return HttpResponse("HEllo")


def upload_json(request):
    if request.method == 'POST':
        form = JSONUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['json_file']

            data_list = json.loads(uploaded_file.read().decode('utf-8'))

            file_db = File(user_id=1)  # TODO: change to actual user id
            file_db.save()

            for data in data_list:
                video_db = Video(
                    host=file_db.id,
                    header=data['header'],
                    title=data['title'],
                    titleUrl=data['titleUrl'],
                    time=data['time'],
                    products=data['products'],
                    activityControls=data['activityControls'],
                )
                video_db.save()
                for subtitle in data['subtitles']:
                    subtitle_db = Subtitle(name=subtitle['name'], url=subtitle['url'])
                    video_db.subtitles.append(subtitle_db)
                video_db.save()

            # Run celery task to proceed videos
            proceed_video.delay(str(file_db.id))

            return HttpResponse("File uploaded")
    else:
        form = JSONUploadForm()

    return render(request, 'upload_json.html', {'form': form})
