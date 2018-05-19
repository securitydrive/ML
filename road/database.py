from __future__ import print_function
import pymysql.connections


class DataBase(object):
    """

    """

    def __init__(self):
        pass

    def connect_db(self, ):
        """

        :return:
        """
        print("connecting...")
        connect = pymysql.connect(user='root',
                                  password='1203',
                                  host='120.24.90.180',
                                  database='app_bak',
                                  use_unicode=True)
        cur = connect.cursor()
        print("database connect success")
        return cur, connect

    def query_data_set(self, cur, query):
        """

        :param cur:
        :param query:
        :return:
        """
        cur.execute(query)
        return cur.fetchall()


if __name__ == '__main__':
    DataBase().connect_db()
