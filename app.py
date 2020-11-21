from collections import defaultdict
import random
from secrets import token_urlsafe

from flask import Flask, session, render_template, request, jsonify, \
	send_from_directory

app = Flask(__name__)
app.config['SECRET_KEY'] = token_urlsafe(random.randint(1, 64))


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


@app.route('/update_count', methods=["GET"])
def update_count():
	print(session)
	if 'id' not in session:
		session['id'] = token_urlsafe(37)
	store_page[request.args['id']].visit(session['id'])
	return send_from_directory('static', 'FF4D00-0.8.png')


@app.route('/get_count', methods=['GET'])
def get_count():
	return jsonify(store_page[request.args['id']].count)


@app.route('/test_page1')
def test_page():
	return render_template('test1.html', id=12345)


@app.route('/test_page2')
def another_page():
	return render_template('test1.html', id=321)


if __name__ == '__main__':
	app.run(host='0.0.0.0')
