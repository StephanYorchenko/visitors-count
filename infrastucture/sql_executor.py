import sqlite3
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