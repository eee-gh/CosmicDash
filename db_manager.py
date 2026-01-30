import sqlite3
from os import path


class DBManager:
    def __init__(self):
        self.connection = sqlite3.connect(str(path.expanduser("~")) + '\\Documents\\CosmicDashRecords.db')
        self.cursor = self.connection.cursor()
        self.table_name = 'records'

    def create_table(self):
        query = f'''
        CREATE TABLE IF NOT EXISTS {self.table_name} (
        id    INTEGER PRIMARY KEY,
        name  TEXT    UNIQUE ON CONFLICT REPLACE
                      NOT NULL,
        time  INTEGER NOT NULL,
        score INTEGER NOT NULL
        );'''
        self.cursor.execute(query)
        self.connection.commit()

    def add_record(self, name, time, score):
        self.create_table()
        query = f'''
        INSERT INTO {self.table_name} ("name", "time", "score")
        VALUES ("{name}", {time}, {score});
        '''
        self.cursor.execute(query)
        self.connection.commit()

    def get_records(self):
        self.create_table()
        query = f'''
        SELECT "name", "time", "score" FROM {self.table_name}
        ORDER BY "score" DESC, "time" DESC, "name" ASC;
        '''
        return self.cursor.execute(query).fetchall()

    def delete_table(self):
        query = f'DROP TABLE IF EXISTS {self.table_name};'
        self.cursor.execute(query)
        self.connection.commit()
