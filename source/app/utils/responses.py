from flask import jsonify, make_response

class Response:
    @staticmethod
    def success(message=None, data=None, status_code=200):
        if status_code == 204:
            return "", 204
        payload = {"success": True}
        if message is not None:
            payload["message"] = message
        if data is not None:
            payload["data"] = data
        return make_response(jsonify(payload), status_code)
    
    @staticmethod
    def error(errors=None, message=None, status_code=400):
        payload = {"success": False}
        if errors:
            payload["errors"] = errors
        if message:
            payload["message"] = message
        return make_response(jsonify(payload), status_code)