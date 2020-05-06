from flask import jsonify, request, url_for

from app import app
from app.models import KV, AccessLog, db


def fulfill_request(key, user_id):
    app.logger.info(key)
    value = KV.query.get(key).value
    al = AccessLog(key=key, value=value, user_id=user_id)
    db.session.add(al)
    db.session.commit()
    return jsonify({key: value})


@app.route('/get', methods=['GET'])
def get():
    key = int(request.args.get('key'))
    user_id = int(request.args.get('user_id'))
    return fulfill_request(key, user_id)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
