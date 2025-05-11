from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/m3u8")
def get_m3u8():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'force_generic_extractor': False,
        'no_warnings': True,
        'simulate': True,
        'forceurl': True,
        'forcejson': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])
            m3u8_links = [f["url"] for f in formats if ".m3u8" in f.get("url", "")]
            return jsonify({"title": info.get("title"), "m3u8_links": m3u8_links})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
