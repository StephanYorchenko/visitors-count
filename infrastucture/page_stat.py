from datetime import datetime


class PageStatistics:
	def __init__(self, storage, id):
		self.storage = storage
		self.id = id

	@classmethod
	def from_data(cls, storage: 'StatStorage', id):
		return PageStatistics(storage, id)

	def visit(self, visitor_id):
		self.storage.update(self, visitor_id, self.get_time())

	def get_count(self, period):
		return self.storage.get_count(self.id, period)

	@staticmethod
	def get_time():
		return f'\'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\''
