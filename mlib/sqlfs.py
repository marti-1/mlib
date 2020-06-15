import sqlite3
import csv
import pandas as pd
import json


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SQLFS:
    def __init__(self):
        self.db = sqlite3.connect(":memory:")
        self.db.row_factory = dict_factory

    def run(self, sql):
        with self.db:
            cur = self.db.cursor()
            cur.execute(sql)
            return True

    def query(self, sql, aswhat='DataFrame'):
        with self.db:
            cur = self.db.cursor()
            cur.execute(sql)
            res = cur.fetchall()
            if aswhat == 'DataFrame':
                return pd.DataFrame(res)
            else:
                return res

    def _fetchone(self, sql):
        with self.db:
            cur = self.db.cursor()
            cur.execute(sql)
            return cur.fetchone()

    def _create_table_from_data(self, name, header, data, schema):
        # convert field values from string to "schema" defined types
        for row in data:
            for field, typefn in schema.items():
                field_idx = header.index(field)
                try:
                    row[field_idx] = typefn(row[field_idx])
                except Exception as e:
                    row[field_idx] = typefn()

        # schema to CREATE TABLE
        create_table = ['CREATE TABLE', name, '(']
        fields = []
        for h in header:
            htype = schema.get(h, str)
            h = h.replace('.', '_')
            if htype == int:
                fields.append(f'{h} INTEGER')
            elif htype == float:
                fields.append(f'{h} REAL')
            else:
                fields.append(f'{h} TEXT')
        create_table.append(','.join(fields))
        create_table.append(')')

        self.run(f'DROP TABLE IF EXISTS {name}')
        self.run(' '.join(create_table))

    def import_obj(self, name, data, filters={}, schema={}):
        header = list(data[0].keys())
        tmp_data = []
        for d in data:
            row = []
            for h in header:
                row.append(d[h])
            tmp_data.append(row)
        data = tmp_data

        data = self._apply_mutate_filters(header, data, filters.get('mutate', None))
        self._create_table_from_data(name, header, data, schema)

        with self.db:
            cur = self.db.cursor()
            placeholder = ','.join(['?'] * len(header))
            cur.executemany(f'INSERT INTO {name} VALUES ({placeholder})', data)

    def import_json(self, fn, name, filters={}, schema={}):
        data = json.load(open(fn, 'r'))
        self.import_obj(name, data, filters, schema)


    def import_ndjson(self, fn, name, filters={}, schema={}):
        data = []
        with open(fn) as f:
            for line in f:
                data.append(json.loads(line))

        self.import_obj(name, data, filters, schema)


    def import_csv(self, fn, name, filters={}, delimiter=',', schema={}):
        data = list(csv.reader(open(fn, 'r'), delimiter=delimiter))
        header = data[0]
        data = data[1:]

        data = self._apply_mutate_filters(header, data, filters.get('mutate', None))
        self._create_table_from_data(name, header, data, schema)

        with self.db:
            cur = self.db.cursor()
            placeholder = ','.join(['?'] * len(header))
            cur.executemany(f'INSERT INTO {name} VALUES ({placeholder})', data)

    def _apply_mutate_filters(self, header, data, filters):
        if filters is None:
            return data

        for row in data:
            for field, fn in filters.items():
                field_idx = header.index(field)
                row[field_idx] = fn(row[field_idx])

        return data

    def head(self, name, n=5):
        return pd.DataFrame(self.query(f'SELECT ROWID, * FROM {name} LIMIT {n}')).set_index('rowid')

    def count(self, name):
        return self._fetchone(f'SELECT COUNT(*) FROM {name}')['COUNT(*)']

    def dbsize(self):
        return self.query('pragma page_count', 'list')[0]['page_count'] * \
               self.query('pragma page_size', 'list')[0]['page_size']
