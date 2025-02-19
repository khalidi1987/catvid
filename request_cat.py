import requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.credentials import Credentials
import io
import os
from google.auth.transport.requests import Request

# Authenticate with the YouTube API using the refresh token
def get_authenticated_service():
    creds = Credentials.from_authorized_user_info({
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET_KEY"),
        "refresh_token": os.getenv("REFRESH_TOKEN"),
        "token": ""
    })

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    
    return build("youtube", "v3", credentials=creds)

# Upload the video to YouTube
def upload_video_to_youtube(video_stream, title="Süße Katze", description="Ein süßes Katzenvideo!", tags=["Katze", "süß"], privacy_status="public"):
    youtube = get_authenticated_service()

    media = MediaIoBaseUpload(video_stream, mimetype="video/mp4", resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "Sweet KITTY portrait": title,
                "enjoy": description,
                "cat": tags,
                "categoryId": "15"  # Pets & Animals category
            },
            "status": {
                "privacyStatus": privacy_status
            }
        },
        media_body=media
    )
    
    response = request.execute()
    print(f"Video uploaded successfully: https://www.youtube.com/watch?v={response['id']}")

# Stream video from Pixabay and upload to YouTube
def stream_and_upload_video_from_url(url):
    # Send a GET request to the video URL
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        print("Streaming video...")
        video_stream = io.BytesIO(response.content)  # Convert the response into a byte stream
        upload_video_to_youtube(video_stream)
    else:
        print(f"Failed to fetch the video. HTTP Status Code: {response.status_code}")

# The video URL from Pixabay
video_url = 'https://cdn.pixabay.com/download/video/167029/cat-head-domestic-cat-portrait-167029.mp4'

# Run the function to stream and upload
stream_and_upload_video_from_url(video_url)
