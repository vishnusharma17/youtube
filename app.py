from flask import Flask, render_template, request, send_file
import subprocess, os, uuid

app = Flask(__name__)

@app.route("/api/download")
def download_api():
    videoURL = request.args.get("url")
    if not videoURL:
        return {"error": "URL is required"}, 400

    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    try:
        subprocess.run([
            "yt-dlp",
            "-f", "best",
            "--merge-output-format", "mp4",
            "-o", filepath,
            "--no-check-certificate",
            videoURL
        ], check=True)
    except Exception as e:
        return {"error": str(e)}, 500

    if not os.path.exists(filepath):
        return {"error": "File not created"}, 500

    return send_file(filepath, as_attachment=True, download_name="video.mp4")

# Render/Linux safe temp storage
DOWNLOAD_DIR = "/tmp/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return render_template("index.html", error="Please enter a valid YouTube/Shorts/Reels URL")

        filename = f"{uuid.uuid4()}.mp4"
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        try:
            result = subprocess.run(
                [
                    "yt-dlp",
                    "-f", "best",
                    "--merge-output-format", "mp4",
                    "-o", filepath,
                    "--no-check-certificate",
                    "--user-agent", "Mozilla/5.0",
                    url
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("Download Log:", result.stdout.decode())
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.decode() if e.stderr else str(e)
            return render_template("index.html", error="Download failed: " + err_msg)

        if not os.path.exists(filepath):
            return render_template("index.html", error="Download failed: File not created")

        return send_file(filepath, as_attachment=True, download_name="video.mp4")

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
