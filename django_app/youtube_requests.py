import requests


def get_video_category(video_id, api_key):
    """Get video category from request get YouTube api.
    Return category id."""
    get_url = f"https://www.googleapis.com/youtube/v3/videos?key={api_key}&id={video_id}&fields=items(id,snippet(categoryId))&part=snippet"

    response = requests.get(get_url)
    response_json = response.json()

    if response.status_code != 200:
        if response.status_code == 403:
            print("Ytb api: Quota daily limit exceeded")
            return None
        print(f"Ytb api: Error while getting video category. Status code: {response.status_code}")
        return 0

    # If empty items list
    if len(response_json["items"]) == 0:
        return 0  # This id doesn't exist

    # Take only needed info
    category_id = response_json["items"][0]["snippet"]["categoryId"]

    return category_id
