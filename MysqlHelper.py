/*
 * C RB Hash Map - Hash Map Implementation in C Language
 * Copyright (c) 2024 Eungsuk Jeon
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
import pymysql
from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB


class MysqlHelper:
    _pool = None

    def __init__(self, host='127.0.0.1', port=3306,
                 db='elvis', user='elvis', password='elvis', charset='utf8'):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.password = password
        self.charset = charset
        self._get_pool()

    def _get_pool(self):
        if not self._pool:
            self._pool = PooledDB(
                creator=pymysql,  # MySQL Connector
                maxconnections=5,  # Maximum number of connections
                mincached=2,  # Minimum number of connections initially
                maxcached=5,  # Maximum number of connections in the pool
                maxshared=3,  # Maximum number of shared connections
                blocking=True,  # Block and wait for a connection if none available
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.db,
                charset=self.charset,
                cursorclass=DictCursor  # Return results as dictionaries
            )

    def connect(self):
        return self._pool.connection()

    def close(self, conn, cursor=None):
        try:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        except Exception as e:
            print(f"Error while closing connection: {str(e)}")

    def update(self, conn, sql, params):
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            raise e
        finally:
            self.close(conn, cursor)

    def query(self, conn, sql, params=None):
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            return cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            self.close(conn, cursor)
