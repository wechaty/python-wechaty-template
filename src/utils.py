from quart import jsonify


def success(data):
    return jsonify({
        "data": data,
        "code": 200
    })

def error(msg):
    return jsonify({
        "msg": msg,
        "code": 500
    })
