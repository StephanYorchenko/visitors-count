from collections import defaultdict
from secrets import token_urlsafe

from flask import session, request, send_from_directory, jsonify


class PageStatistics:
    def __init__(self):
        self.visitors = set()

    def visit(self, visitor_id):
        was_visited = visitor_id in self.visitors
        self.visitors.add(visitor_id)
        return was_visited

    @property
    def count(self):
        return len(self.visitors)


store_page = defaultdict(PageStatistics)


def update_count():
    if "id" not in session:
        session["id"] = token_urlsafe(37)
    store_page[request.args["id"]].visit(session["id"])
    return send_from_directory("static", "FF4D00-0.8.png")


def get_count():
    return jsonify(store_page[request.args["id"]].count)
