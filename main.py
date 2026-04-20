import os
from flask import Flask, render_template_string, request
from googleapiclient.discovery import build

app = Flask(__name__)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

html_template = """
<!DOCTYPE html>
<html lang="si">
<head>
    <meta charset="UTF-8">
    <title>Sumiya App Genesis</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #0f0f0f; color: white; text-align: center; margin: 0; padding: 20px; }
        .header { padding: 30px; background: linear-gradient(45deg, #ff0000, #b30000); border-radius: 15px; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(255,0,0,0.3); }
        input { padding: 15px; width: 60%; border-radius: 30px; border: none; outline: none; font-size: 16px; margin-bottom: 10px; }
        button { padding: 15px 30px; border-radius: 30px; border: none; background: white; color: #ff0000; cursor: pointer; font-weight: bold; transition: 0.3s; }
        button:hover { background: #e0e0e0; transform: scale(1.05); }
        .video-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 25px; padding: 20px; }
        .video-card { background: #1e1e1e; padding: 15px; border-radius: 15px; box-shadow: 0 10px 20px rgba(0,0,0,0.5); }
        iframe { width: 100%; height: 200px; border-radius: 10px; border: none; }
        h3 { font-size: 14px; margin-top: 15px; color: #f1f1f1; }
        .message { padding: 20px; font-size: 18px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Sumiya App Genesis</h1>
        <p>ඔයාගේම YouTube සර්ච් ඇප් එක</p>
        <form action="/" method="GET">
            <input type="text" name="q" placeholder="වීඩියෝ එකේ නම මෙතන ටයිප් කරන්න..." required>
            <br>
            <button type="submit">Search (සොයන්න)</button>
        </form>
    </div>
    {{ message|safe }}
    <div class="video-grid">
        {% for video in videos %}
        <div class="video-card">
            <iframe src="https://www.youtube.com/embed/{{ video.id.videoId }}" allowfullscreen></iframe>
            <h3>{{ video.snippet.title }}</h3>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    query = request.args.get('q')
    videos = []
    message = ""
    if query:
        try:
            if not YOUTUBE_API_KEY:
                return "Error: YouTube API Key is not set in Koyeb settings!"
            
            youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
            req = youtube.search().list(q=query, part='snippet', type='video', maxResults=12)
            res = req.execute()
            videos = res.get('items', [])
            
            if not videos:
                message = '<div class="message"><h2>Result නෑ මචෝ 😢</h2></div>'
                
        except Exception as e:
            print(f"Error: {e}")
            return f"API Error: {e}"
    return render_template_string(html_template, videos=videos, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
