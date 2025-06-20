from youtube_transcript_api import YouTubeTranscriptApi
from langchain_community.document_loaders.youtube import YoutubeLoader

video_id = "qbZsRYvUJoY"
url ="https://www.youtube.com/watch?v=qbZsRYvUJoY"
# try:
#     transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
#     print("Available languages:", [t.language_code for t in transcript_list])
# except Exception as e:
#     print("字幕一覧の取得に失敗:", e)


loader = YoutubeLoader.from_youtube_url(
                        url,
                        language=["ja"],  # 英語→日本語の優先順位で字幕を取得
                        # add_video_info=False # タイトルや再生数などのメタデータも取得するオプション。バージョンのせいかエラーになるのでコメントアウト
                        )
res = loader.load()
print(res)