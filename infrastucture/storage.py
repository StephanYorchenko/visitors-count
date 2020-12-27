from infrastucture.page_stat import PageStatistics
from infrastucture.sql_executor import SQLExecutor


class StatStorage:
    def __init__(self, sql_executor: SQLExecutor):
        self.database = sql_executor
        self.pages = {}

    def __getitem__(self, item):
        if item not in self.pages:
            self.pages[item] = self.get_all_stat(item)
        return self.pages[item]

    def update(self, page: "PageStatistics", visitor_id, time):
        self.database.try_insert(
            "visits",
            visit_time=time,
            page_id=page.id,
            client_id=f'"{visitor_id}"'
        )

    def get_all_stat(self, page_id):
        return PageStatistics.from_data(self, page_id)

    def get_count(self, page_id, period):
        return dict(
            all=self.database.count_all(page_id, period),
            unique=self.database.count_all(page_id, period, unique=True),
        )
