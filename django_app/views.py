from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import JSONUploadForm, CreateUserForm, LoginForm

import json
from .models.mongo import File, Video, Subtitle
from .models.postgres import UserProfile, WatchRecord
from .tasks import proceed_video

from django_pandas.io import read_frame
from .chart_generation import category_trend_chart, category_total_watched_chart, category_trend_chart

def home(request):
    return HttpResponse("HEllo")


def register_page(request):
    """User registration using form."""
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            pass  # TODO: handle invalid form

    context = {'form': form}
    return render(request, 'register.html', context)


def login_page(request):
    """User login using form."""
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('upload_json')
            else:
                pass  # TODO: handle invalid login

    context = {'form': form}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def upload_json(request):
    """User upload json file using form. Json objects are saved in mongo db.
    Celery task proceed_video is called to proceed videos in json file."""
    if request.method == 'POST':
        form = JSONUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['json_file']

            data_list = json.loads(uploaded_file.read().decode('utf-8'))  # TODO: think about encoding format

            # Create user profile in postgres
            user_profile = UserProfile.objects.create(user_id=request.user)
            user_profile.save()

            file_db = File(user_id=request.user.id, user_profile_id=user_profile.id)
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


@login_required(login_url='login')
def profiles_page(request):
    #  Print list of all user uploaded files with status
    files = File.objects.filter(user_id=request.user.id)

    context = {'files': files}
    return render(request, 'profiles.html', context)


@login_required(login_url='login')
def visualize_profile(request, profile_id):
    # Get all watch records for profile
    profile_watch_records = WatchRecord.objects.filter(user_profile_id=profile_id)

    # Join with Video Chanel and Category
    profile_watch_records = profile_watch_records.select_related('video')
    profile_watch_records = profile_watch_records.select_related('video__chanel')
    profile_watch_records = profile_watch_records.select_related('video__category')

    # Take only needed columns
    # WatchRecord time, Video name, Chanel name, Category name
    profile_watch_records = profile_watch_records.values(
        'time', 'video__name', 'video__chanel__name', 'video__category__name'
    )

    df = read_frame(profile_watch_records)

    category_total_watched = category_total_watched_chart(df).to_html(full_html=False, include_plotlyjs='cdn')
    category_trend = category_trend_chart(df).to_html(full_html=False, include_plotlyjs='cdn')

    context = {
        'category_trend': category_trend,
        'category_total_watched': category_total_watched
    }
    return render(request, 'visualize_profile.html', context)


@login_required(login_url='login')
def delete_profile(request, profile_id):
    """Delete user profile.
    Remove watch records from postgres.
    Remove file related to profile from mongo."""

    # Delete profile from postgres. All watch records will be deleted by cascade
    user_profile = UserProfile.objects.get(id=profile_id)  # TODO: handle not found
    user_profile.delete()

    # Find file that have user_profile_id
    files = File.objects.filter(user_profile_id=profile_id)
    for file in files:
        # Find and remove all Videos that have host=file.id
        videos = Video.objects.filter(host=file.id)
        for video in videos:
            video.delete()

        file.delete()

    return redirect('profiles')
