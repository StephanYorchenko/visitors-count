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
        if period != 'ALL_STAT':
            return dict(
                all=self.database.count_all(page_id, period),
                unique=self.database.count_all(page_id, period, unique=True),
            )
        print('here')
        return dict(
                all_today=self.database.count_all(page_id, "-1 day"),
                unique_today=self.database.count_all(page_id, "-1 day", unique=True),
                all_28d=self.database.count_all(page_id,"-28 day"),
                unique_28d=self.database.count_all(page_id, "-28 day",
                                                     unique=True),
                all=self.database.count_all(page_id, "-4000 year"),
                unique=self.database.count_all(page_id, "-4000 year",
                                                     unique=True),
        )

    @classmethod
    def make_with_executor(cls, executor):
        return cls(executor)
