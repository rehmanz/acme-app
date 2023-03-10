from flask import Flask, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import json
import logging

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class AccessEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(64))
    xff = db.Column(db.String(64))
    user_agent = db.Column(db.String(1024))
    access_time = db.Column(db.DateTime, default=datetime.utcnow)
    path = db.Column(db.String(1024))

@app.errorhandler(404)
def index(_):
    remote_addr = request.remote_addr
    xff = request.headers.get("X-Forwarded-For", "")
    user_agent = request.headers.get("User-Agent", "")
    path = request.path

    entry = AccessEntry(ip=remote_addr, xff=xff, user_agent=user_agent, path=path)
    logging.debug("entry: %s" %entry)
    try:
        db.session.add(entry)
        db.session.commit()
    except Exception as e:
        raise Exception("Unable to add a record in database")


    entries = AccessEntry.query.order_by(AccessEntry.access_time.desc()).limit(10)
    ret = [
        {
            "ip": entry.ip,
            "xff": entry.xff,
            "user_agent": entry.user_agent,
            "path": entry.path,
            "time": entry.access_time.isoformat(),
        }
        for entry in entries
    ]

    return json.dumps(ret)


@app.route("/_healthz")
def health():
    msg = json.dumps({"status": "HEALTHY", "count": AccessEntry.query.count()})
    logging.debug("msg: %s" %msg)
    return msg


def main():
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    app.run(host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()
