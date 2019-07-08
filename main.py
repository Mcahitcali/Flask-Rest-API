from __future__ import unicode_literals
from flask import Flask
from flask_restful import Api, Resource
from pathlib import Path
import youtube_dl
import glob


application = Flask(__name__)
api = Api(app=application)

ydl_path = str(Path().absolute())+"/File/"
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': ydl_path+'%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

@application.route("/")
def home():
    html = ''
    files = [f for f in glob.glob(ydl_path + "**/*.mp3", recursive=True)]
    for file in files:
        html += f'<a href="{file}"> click here for open file</a></br>'

    return html
class Base_URL(Resource):
    def get(self, url_id):
        convert_url = f"https://www.youtube.com/watch?v={url_id}"
        file_path = str(Path().absolute())+"/File/"
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([convert_url])
            ydl_info = ydl.extract_info(convert_url, download=False)
            file_path = ydl_info.get("title",None)+".mp3"

        return f"<h1>Url is converted</h1></br>Converted Url: {file_path}", 200
        
api.add_resource(Base_URL, "/url/<string:url_id>")
application.run(debug=True)