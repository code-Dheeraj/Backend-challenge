from flask import Response, jsonify, make_response


class APIResponse(Response):
    @classmethod
    def respond(cls, data):
        return make_response(jsonify(data=data))

class APIResponse(Response):
    @classmethod
    def respond(cls, data):
        # Ensure the response structure matches what is expected in the test
        return make_response(jsonify(data=data), 200)
