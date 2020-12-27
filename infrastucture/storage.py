import sqlite3
from datetime import datetime
from os.path import isfile


class SQLExecutor:
	def __init__(self, database_name="database.db"):
		self.database_name = database_name
		self._exist_or_create()

	def execute(self, sql_string):
		with sqlite3.connect(self.database_name) as connection:
			cursor = connection.cursor()
			result = list(cursor.execute(sql_string))
			cursor.fetchall()
			cursor.close()
		return result

	def select(self, table, *args, **kwargs):
		required_fields = ', '.join(args) if args else '*'
		criteria = ' and '.join(
				list(map(lambda a: f"{a[0]}={a[1]}", kwargs.items()))) or 'id'
		sql = f"SELECT {required_fields} FROM {table} WHERE {criteria};"
		return self.execute(sql)

	def update(self, table, value_update, **kwargs):
		criteria = ' and '.join(
				list(map(lambda a: f"{a[0]}={a[1]}", kwargs.items()))) or 'id'
		sql = f'UPDATE {table} ' \
			  f'SET {value_update[0]}={value_update[1]} WHERE {criteria};'
		return self.execute(sql)

	def try_insert(self, table, **kwargs):
		sql = f"INSERT OR IGNORE INTO {table} " \
			  f"({', '.join(kwargs.keys())}) " \
			  f"VALUES ({', '.join(map(str, kwargs.values()))})"
		return self.execute(sql)

	def insert_or_update(self, table, value_update, **kwargs):
		self.update(table, value_update, **kwargs)
		if not self.select(table, **kwargs):
			kwargs.update({value_update[0]: value_update[1]})
			self.try_insert(table, **kwargs)

	def _exist_or_create(self):
		if isfile(self.database_name):
			return
		conn = sqlite3.connect(self.database_name)
		conn.close()
		table_users = """CREATE TABLE visits (
					page_id INTEGER,
					client_id TEXT,
					visit_time TEXT
				);"""
		self.execute(table_users)

	def select_for_days(self, period, page_id):
		sql = f"""SELECT client_id FROM visits
		 		  WHERE visit_time
		 		  BETWEEN datetime('now', '{period}') 
		 		  AND datetime('now', 'localtime') 
		 		  AND page_id = '{page_id}';"""
		return self.execute(sql)

	def count_all(self, page_id, period, unique=False):
		selection = self.select_for_days(period, page_id)
		if not selection:
			return 0
		if not unique:
			return len(selection)
		return len(set(map(lambda x: x[0], selection)))


class StatStorage:
	def __init__(self, sql_executor: SQLExecutor):
		self.database = sql_executor
		self.pages = {}

	def __getitem__(self, item):
		if item not in self.pages:
			self.pages[item] = self.get_all_stat(item)
		return self.pages[item]

	def update(self, page: 'PageStatistics', visitor_id, time):
		self.database.try_insert(
				"visits",
				visit_time=time,
				page_id=page.id, client_id=f"\"{visitor_id}\"")

	def get_all_stat(self, page_id):
		return PageStatistics.from_data(self, page_id)

	def get_count(self, page_id, period):
		return dict(
				all=self.database.count_all(page_id, period),
				unique=self.database.count_all(page_id, period, unique=True)
		)


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
