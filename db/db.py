import sqlite3

def with_connection(f):
    def with_connection_(*args, **kwargs):
        conn = sqlite3.connect('raspa.db')
        cur = conn.cursor()
        result = f(cur, *args, **kwargs)
        conn.commit()
        conn.close()
        return result
    return with_connection_

@with_connection
def db_insert_new_user(cur, user_id, group_name):
    cur.execute("INSERT OR REPLACE INTO users VALUES ('%s', '%s')" % (user_id, group_name))

@with_connection
def db_delete_user(cur, user_id):
    cur.execute("DELETE FROM users WHERE user_id='%s'" % user_id)

@with_connection
def db_user_exist(cur, user_id):
    cur.execute("SELECT * FROM users WHERE user_id = '%s'" % user_id)
    result = cur.fetchone()
    if result is None:
        return False
    return True

@with_connection
def db_get_users(cur):
    cur.execute("SELECT user_id FROM users ")
    result = cur.fetchall()
    return result

@with_connection
def db_get_user_group_name(cur, user_id):
    cur.execute("SELECT group_name FROM users WHERE user_id = '%s'" % user_id)
    result = cur.fetchone()
    return result[0]

@with_connection
def db_set_user_group(cur, user_id, user_group):
    cur.execute("UPDATE users SET group_name = '%s' WHERE user_id = '%s'" % (user_group, user_id))

