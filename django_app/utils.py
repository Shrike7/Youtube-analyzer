from .models.mongo import Video, Subtitle
from .models.postgres import WatchRecord

from django_pandas.io import read_frame


def proceed_json_video_data(file_db, data):
    """Help function for upload_json view.
    Proceed json object video and save it to mongo.
    Skip unwanted data."""
    # Check if ActivityControls is YouTube watch history
    if data['activityControls'][0] != 'YouTube watch history':
        return
    # Skip if there is details
    if 'details' in data:
        return

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


def get_dataframe_to_visualize(profile_id):
    """Help function for visualize_profile view.
    Get data from postgres related to profile.
    Join with Video Channel and Category.
    Make some data preprocessing.
    Return pandas dataframe to visualize."""
    # Get all watch records for profile
    profile_watch_records = WatchRecord.objects.filter(user_profile_id=profile_id)

    # Join with Video Channel and Category
    profile_watch_records = profile_watch_records.select_related('video')
    profile_watch_records = profile_watch_records.select_related('video__channel')
    profile_watch_records = profile_watch_records.select_related('video__category')

    # Take only needed columns
    # WatchRecord time, Video name, Channel name, Category name
    profile_watch_records = profile_watch_records.values(
        'time', 'video__name', 'video__channel__name', 'video__category__name'
    )

    df = read_frame(profile_watch_records)

    # For all time change timezone to user timezone
    df['time'] = df['time'].dt.tz_convert('Europe/Prague')  # TODO: get user timezone

    return df
