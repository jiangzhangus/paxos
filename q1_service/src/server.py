from flask import Flask, escape, jsonify
from flask import redirect, request, render_template

from handler import WebHandler


app = Flask(__name__)


# -------------- RestFull API ------------
@app.route('/messages', methods=['POST'])
def add_message():
    """add a new message"""

    utils = WebHandler()
    message_key = "message"

    if request.data!= b'':
        try:
            dict_data = eval(request.data)
            msg = dict_data[message_key]
            hash_value = utils.hash_and_save(msg)
            return utils.ret_JSON('hash', hash_value)
        except:
            # curl -X POST -H "Content-Type: application/json" -d "{\"message\":\"foo\"}" http://127.0.0.1:5000/messages
            # on windows curl command should escape -d using ", single ' will not work.
            err_msg = "failed to load from request.data. On Windows, please use only double quotes. Single quote doesn't work"
            return utils.ret_JSON('error', err_msg)
    else:
        try:
            for m in request.values:
                m = eval(m)
                if len(m) > 0:
                    msg = m[message_key]
                    hash_value = utils.hash_and_save(msg)
                    return utils.ret_JSON('hash', hash_value)
        except:
            pass

        # no value is valid
        err_msg = "request.values doesn't contain key " + message_key
        return utils.ret_JSON('error', err_msg)


@app.route('/messages/<string:hash>', methods=['GET'])
def get_message(hash):
    """get message by hash value"""
    utils = WebHandler()
    msg = utils.get_data(hash)
    if msg is None: # failed to find the message
        return utils.ret_JSON('error', "Message not found")
    else:
        return utils.ret_JSON('message', msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)