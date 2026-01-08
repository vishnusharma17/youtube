from flask import Flask, render_template, request, send_file
import subprocess, os, uuid

app = Flask(__name__)

DOWNLOAD_DIR = "/tmp/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/api/download")
def download_api():
    videoURL = request.args.get("url")
    if not videoURL:
        return {"error": "URL is required"}, 400

    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    try:
        result = subprocess.run([
            "yt-dlp",
            videoURL,
            "-f", "b",
            "-o", filepath,
            "--merge-output-format", "mp4",
            "--no-check-certificate",
            "--user-agent", "Mozilla/5.0"
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print("STDOUT:", result.stdout.decode())
        print("STDERR:", result.stderr.decode())

    except subprocess.CalledProcessError as e:
        return {"error": "Download failed: " + e.stderr.decode()}, 500

    if not os.path.exists(filepath):
        return {"error": "File not created"}, 500

    response = send_file(filepath, as_attachment=True, download_name="video.mp4")

    try:
        os.remove(filepath)
    except:
        pass

    return response

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
