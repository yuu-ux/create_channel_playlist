import googleapiclient.discovery
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

# APIキーの読み込み
load_dotenv()
api_key = os.getenv("API_KEY")

# APIクライアントを初期化
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

# チャンネルIDを指定
channel_id = "CHANNEL_ID" # 取得したいチェンネルのIDを取得する

# チャンネルのアップロード動画を取得する
request = youtube.search().list(
    part="snippet",
    channelId=channel_id,
    maxResults=50,  # 最大50件まで取得
    type="video"
)
response = request.execute()

# 動画IDのリストを作成
video_ids = [item['id']['videoId'] for item in response['items']]

# OAuth 2.0 認証のスコープ設定
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# OAuth 2.0 認証フローを開始 (client_secrets.json をプロジェクトに配置してください)
flow = InstalledAppFlow.from_client_secrets_file(
    'client_secrets.json', scopes)  # client_secrets.jsonファイルのパス
credentials = flow.run_local_server(port=0)  # ローカルサーバーで認証を実行

# YouTube API クライアントを作成
youtube = build("youtube", "v3", credentials=credentials)

# プレイリストを作成
playlist_request = youtube.playlists().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": "TITLE", # タイトル
        },
        "status": {
            "privacyStatus": "private"  # 公開設定
        }
    }
)
playlist_response = playlist_request.execute()

# プレイリストIDを取得
playlist_id = playlist_response["id"]

# 各動画をプレイリストに追加
for video_id in video_ids:
    add_video_request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id,
                }
            }
        }
    )
    add_video_request.execute()

print(f"プレイリストが作成されました: https://www.youtube.com/playlist?list={playlist_id}")
