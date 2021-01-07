import os
import tempfile
import unittest
from io import BytesIO

from app import AppFactory
from image_generator import ImageGenerator
from infrastucture import SQLExecutor, StatStorage
from routes import RoutesFactory, RequestHandler


class AppTests(unittest.TestCase):
	def setUp(self) -> None:
		self.fd, self.name = tempfile.mkstemp(suffix='.db')
		self.sql_executor = SQLExecutor(self.name, debug=True)
		self.storage = StatStorage.make_with_executor(self.sql_executor)
		self.image_generator = ImageGenerator()
		routes = RoutesFactory.make_routes(self.storage,
										   self.image_generator,
										   RequestHandler)
		self.app = AppFactory.make_app(routes)

	def tearDown(self) -> None:
		os.close(self.fd)
		os.unlink(self.name)

	def test_update_table(self):
		with open(self.app.static_folder + '/FF4D00-0.8.png', 'rb') as img1:
			img = BytesIO(img1.read())

		with self.app.test_client() as c:
			rv = c.get('/update_count?id=1')
		img.seek(0)
		self.assertEqual(rv.data, img.read())
		self.assertDictEqual(self.storage[1].get_count("-4000 year"),
							 {'all': 1, 'unique': 1})

	def test_few_update_requests(self):
		with open(self.app.static_folder + '/FF4D00-0.8.png', 'rb') as img1:
			img = BytesIO(img1.read())

		with self.app.test_client() as c:
			c.get('/update_count?id=1')
			rv1 = c.get('/update_count?id=1')

		self.assertEqual(rv1.data, img.read())
		self.assertDictEqual(self.storage[1].get_count("-4000 year"),
							 {'all': 2, 'unique': 1})

	def test_get_count_all(self):
		with self.app.test_client() as c:
			rv = c.get('/get_count?id=1&period=all')
			data = rv.get_json()
			self.assertDictEqual(data, {'all': 0, 'unique': 0})
			c.get('/update_count?id=1')
			rv = c.get('/get_count?id=1&period=all')
			data = rv.get_json()
			self.assertDictEqual(data, {'all': 1, 'unique': 1})
			c.get('/update_count?id=1')
			rv = c.get('/get_count?id=1&period=all')
			data = rv.get_json()
			self.assertDictEqual(data, {'all': 2, 'unique': 1})

	def test_get_by_today(self):
		self.sql_executor.execute(
				"INSERT INTO visits (page_id, client_id, visit_time) "
				"VALUES (1, 'qwertyui', '1970-01-06 21:30:58')")
		with self.app.test_client() as c:
			rv = c.get('/get_count?id=1&period=today')
			data = rv.get_json()
			self.assertDictEqual(data, {'all': 0, 'unique': 0})
			c.get('/update_count?id=1')
			rv = c.get('/get_count?id=1&period=today')
			data = rv.get_json()
			self.assertDictEqual(data, {'all': 1, 'unique': 1})
			c.get('/update_count?id=1')
			rv = c.get('/get_count?id=1&period=today')
			data = rv.get_json()
			self.assertDictEqual(data, {'all': 2, 'unique': 1})
			rv = c.get('/get_count?id=1&period=all')
			data = rv.get_json()
			self.assertDictEqual(data, {'all': 3, 'unique': 2})


if __name__ == '__main__':
	unittest.main()
