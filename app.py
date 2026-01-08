from flask import Flask, render_template, request, send_file
import subprocess, os, uuid

app = Flask(__name__)

DOWNLOAD_DIR = "/tmp/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/api/download")
def download_api():
    url = request.args.get("url")
    if not url:
        return {"error": "URL is required"}, 400

    # Instagram always works
    if "instagram.com" in url:
        filename = f"{uuid.uuid4()}.mp4"
        filepath = os.path.join(DOWNLOAD_DIR, filename)
        try:
            subprocess.run([
                "yt-dlp", "-f", "b", "-o", filepath,
                "--merge-output-format", "mp4",
                "--no-check-certificate",
                "--user-agent", "Mozilla/5.0",
                url
            ], check=True)
        except Exception as e:
            return {"error": str(e)}, 500

        if not os.path.exists(filepath):
            return {"error": "File not created"}, 500

        return send_file(filepath, as_attachment=True, download_name="video.mp4")

    # YouTube Shorts ko skip karo (server se nahi)
    if "youtube.com/shorts" in url:
        return {"error": "Shorts download is only supported from browser preview, server download disabled for stability."}, 200

    # Baaki YouTube videos try karo
    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    try:
        subprocess.run([
            "yt-dlp", "-f", "b", "-o", filepath,
            "--merge-output-format", "mp4",
            "--no-check-certificate",
            "--user-agent", "Mozilla/5.0",
            url
        ], check=True)
    except Exception as e:
        return {"error": str(e)}, 500

    if not os.path.exists(filepath):
        return {"error": "File not created"}, 500

    return send_file(filepath, as_attachment=True, download_name="video.mp4")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
