from flask import Flask, escape, jsonify
from flask import session, url_for, make_response

import hashlib
import sqlite3

# module level variable, so that we keep data across multiple requests.
# When the program is closed, the data will be gone as well
db_conn = None


class WebHandler(object):
    def __init__(self):
        global db_conn
        if db_conn is None:
            db_conn = sqlite3.connect(':memory:')
        self.db_conn = db_conn

    def __ensure_table(self):
        # make sure the table exists
        # sqlite will treat "varchar" as TEXT type
        # use varchar here for better portability
        # sha256 in hexadecimal uses 64 chars
        sql = "create table if not exists messages(hash_str varchar(64) NOT NULL, msg_str TEXT)"
        self.db_conn.execute(sql)

    def __save_data(self, hash, message):
        """save a hash-message pair to database"""
        self.__ensure_table()
        sql = "INSERT INTO messages VALUES(?,?)"
        print("saving data in __save_data()")
        self.db_conn.execute(sql, (hash, message))

    def get_data(self, hash_value):
        """get message from db, using key (hash string)"""
        print("trying to get data by " + hash_value)
        self.__ensure_table()
        sql = "SELECT hash_str, msg_str FROM messages WHERE hash_str = ?"
        results = self.db_conn.execute(sql, (hash_value,))

        for row in results:
            #print("---get data:" + str(row))
            return row[1]
        return None

    def __do_hashing(self, msg):
        hash_obj = hashlib.sha256()
        msg = msg.encode('utf-8') # encode unicode string to bytes
        hash_obj.update(msg)
        hash_value = hash_obj.hexdigest()
        return hash_value

    def hash_and_save(self, msg):
        if not msg:
            return ''
        hash_value = self.__do_hashing(msg)
        self.__save_data(hash_value, msg)
        return hash_value

    def ret_JSON(self, value_type, value):
        ret_code = 200
        json_str = ''

        if value_type == 'error':
            ret_code = 404
            json_str = jsonify(error_msg = value)
        elif value_type == 'hash':
            json_str = jsonify(digest = value)
        else:
            json_str = jsonify(message = value)

        return make_response(json_str, ret_code)
