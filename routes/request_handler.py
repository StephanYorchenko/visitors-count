from secrets import token_urlsafe

from flask import request, jsonify, abort, \
	send_file, make_response, send_from_directory


class RequestHandler:
	periods = {"today": "-1 day", "28d": "-28 day", "all": "-4000 year"}

	def __init__(self, stat_storage, image_generator):
		self.store_page = stat_storage
		self.image_generator = image_generator

	def update_count(self):
		page_id = request.args.get("id")
		response = make_response(
				send_from_directory("static", "FF4D00-0.8.png")
		)
		client_id = request.cookies.get("id")
		if client_id is None:
			client_id = token_urlsafe(37)
			response.set_cookie("id", str(client_id), samesite='Lax',
								secure=True)
		self.store_page[page_id].visit(client_id)
		return response

	def get_count(self):
		page_id = request.args.get("id")
		period = request.args.get("period") or "all"
		if not id or period not in self.periods:
			raise abort(404)
		period = self.periods[period]
		return jsonify(self.store_page[page_id].get_count(period))

	def get_image(self):
		page_id = request.args.get("id")
		period = request.args.get("period") or "all"
		if not id or period not in self.periods:
			raise abort(404)
		period = self.periods[period]
		a = self.store_page[page_id].get_count(period)
		print(a)
		stat = '\n'.join(map(str, a.values()))
		response = make_response(
				send_file(self.image_generator.make_image(stat), as_attachment=True,
						  attachment_filename="stat.png")
		)
		return response
