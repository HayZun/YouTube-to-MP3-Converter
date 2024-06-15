from flask import Flask, request, render_template, send_file
from pytube import YouTube
import moviepy.editor as mp
import os

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    url = request.form["url"]
    video = YouTube(url)
    stream = video.streams.filter(only_audio=True).first()
    out_file = stream.download(output_path=".")

    base, ext = os.path.splitext(out_file)
    new_file = base + ".mp3"

    clip = mp.AudioFileClip(out_file)
    clip.write_audiofile(new_file)
    clip.close()

    # Envoyer le fichier MP3 à l'utilisateur en tant que téléchargement
    response = send_file(new_file, as_attachment=True)

    # Supprimer le fichier vidéo temporaire après l'envoi réussi du fichier MP3
    os.remove(out_file)
    os.remove(new_file)

    return response


if __name__ == "__main__":
    app.run(debug=True)
