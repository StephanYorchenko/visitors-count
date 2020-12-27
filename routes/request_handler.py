from secrets import token_urlsafe

from flask import request, send_from_directory, jsonify, make_response, abort


class RequestHandler:
	periods = {
			"today": "-1 day",
			"28d": "-28 day",
			"all": "-4000 year"
	}

	def __init__(self, stat_storage):
		self.store_page = stat_storage

	def update_count(self):
		page_id = request.args.get("id")
		response = make_response(
				send_from_directory("static", "FF4D00-0.8.png"))
		client_id = request.cookies.get('id')
		if client_id is None:
			client_id = token_urlsafe(37)
			response.set_cookie('id', str(client_id), max_age=9999999)
		self.store_page[page_id].visit(client_id)
		return response

	def get_count(self):
		page_id = request.args.get('id')
		period = request.args.get('period') or 'all'
		if not id:
			raise abort(404)
		period = self.periods[period]
		return jsonify(self.store_page[page_id].get_count(period))
