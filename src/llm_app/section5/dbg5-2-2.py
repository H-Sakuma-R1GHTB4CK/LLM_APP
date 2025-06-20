# from youtube_transcript_api import YouTubeTranscriptApi

# # URL から video_id を取り出すか、直接動画IDを入れてください
video_id = "qbZsRYvUJoY"

# try:
#     # 利用可能な字幕言語一覧を再確認
#     transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
#     print("Available languages:", [t.language_code for t in transcript_list])

#     # ja のトランスクリプトを取得してみる
#     transcript = transcript_list.find_transcript(['ja'])
#     segments = transcript.fetch()
#     print("Fetched segments (先頭5つ):", segments[:5])
# except Exception as e:
#     import traceback; traceback.print_exc()


import requests
from bs4 import BeautifulSoup

# url = "https://www.youtube.com/watch?v=qbZsRYvUJoY"
# resp = requests.get(url)
# soup = BeautifulSoup(resp.text, "html.parser")

# tracks = soup.find_all("track")
# for t in tracks:
#     print(t.attrs)



# resp = requests.get(
#     "http://video.google.com/timedtext",
#     params={"v": video_id, "lang": "ja"}
# )
# print("Status code:", resp.status_code)
# print("Response text:", repr(resp.text))

from youtube_transcript_api import YouTubeTranscriptApi

try:
    segments = YouTubeTranscriptApi.get_transcript(video_id, languages=["ja"])
    print("Fetched segments (先頭5つ):", segments[:5])
except Exception as e:
    import traceback; traceback.print_exc()
