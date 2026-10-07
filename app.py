import argparse
import json
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import BadRequest

from shipping import calculate_fee

ROOT = Path(__file__).resolve().parent


def create_app() -> Flask:
    app = Flask(__name__)
    app.json.ensure_ascii = False
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024
    records = json.loads((ROOT / "fixtures" / "tracking.json").read_text(encoding="utf-8"))

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/health")
    def health():
        return jsonify(ok=True, app="postal-workshop")

    @app.post("/api/quote")
    def quote():
        if not request.is_json:
            return jsonify(error="請使用 JSON 格式送出。"), 400
        try:
            data = request.get_json()
        except BadRequest:
            return jsonify(error="JSON 格式不正確。"), 400
        if not isinstance(data, dict):
            return jsonify(error="請提供重量與寄送服務。"), 400
        try:
            fee = calculate_fee(data.get("weight_grams"), data.get("service"))
        except ValueError as error:
            return jsonify(error=str(error)), 400
        return jsonify(fee=fee, currency="TWD")

    @app.get("/tracking")
    def tracking():
        return render_template("tracking.html")

    @app.get("/api/tracking/<mail_id>")
    def tracking_record(mail_id: str):
        for record in records:
            if record["mail_id"] == mail_id:
                return jsonify(record)
        return jsonify(error="查無資料", mail_id=mail_id), 404

    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Local-only workshop application")
    parser.add_argument("--port", type=int, default=5050)
    args = parser.parse_args()
    create_app().run(host="127.0.0.1", port=args.port, debug=False)
