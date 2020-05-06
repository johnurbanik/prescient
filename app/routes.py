from flask import jsonify, request

from app import app
from app.models import KV, AccessLog, db


@app.route('/get', methods=['GET'])
def get():
    key = request.args.get('key')
    user_id = request.args.get('user_id')
    return fulfill_request(key, user_id)


def fulfill_request(key, user_id):
    value = KV.query
    al = AccessLog(key=key, value=value, user_id=user_id)
    db.session.add(al)
    db.session.commit()
    return jsonify(**{key: value})
