from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

# Authentifizierung für YouTube API
def get_authenticated_service():
    from google.oauth2.credentials import Credentials
    creds = Credentials.from_authorized_user_info({
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET_KEY"),
        "refresh_token": os.getenv("REFRESH_TOKEN"),
        "token": ""
    })
    return build("youtube", "v3", credentials=creds)

# Video auf YouTube hochladen
def upload_video(file_path, title="Süße Katze", description="Ein süßes Katzenvideo!", tags=["Katze", "süß"], privacy_status="public"):
    youtube = get_authenticated_service()
    
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": "15"
            },
            "status": {
                "privacyStatus": privacy_status
            }
        },
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )
    response = request.execute()
    print(f"Video hochgeladen: https://www.youtube.com/watch?v={response['id']}")

upload_video("katzenvideo.mp4")
