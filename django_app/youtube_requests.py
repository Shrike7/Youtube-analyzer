import requests
from decouple import config


def get_video_category(video_id):
    """Get video category from request get YouTube api.
    Return category id."""
    api_key = config("API_KEY")
    get_url = f"https://www.googleapis.com/youtube/v3/videos?key={api_key}&id={video_id}&fields=items(id,snippet(categoryId))&part=snippet"

    response = requests.get(get_url)
    response_json = response.json()

    if response.status_code != 200:
        if response.status_code == 403:
            print("Ytb api: Quota daily limit exceeded")
            return None

    # If empty items list
    if len(response_json["items"]) == 0:
        print(f"Ytb api: Video {video_id} empty items list")
        return None

    # Take only needed info
    category_id = response_json["items"][0]["snippet"]["categoryId"]

    return category_id
