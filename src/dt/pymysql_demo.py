import hashlib

from dt.DB_utils import POOL
import pymysql


def create_conn():
    conn = POOL.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    return conn, cursor


def close_conn(conn, cursor):
    conn.close()
    cursor.close()


def select_all(sql, args):
    conn, cur = create_conn()
    cur.execute(sql, args)
    result = cur.fetchall()
    print(result)
    close_conn(conn, cur)
    return result


def select_token(sql, args):
    conn, cur = create_conn()
    cur.execute(sql, args)
    result = cur.fetchall()
    print('{} token: {}'.format(args, result))
    close_conn(conn, cur)
    return result


def token_insert(sql, args):
    conn, cur = create_conn()
    try:
        cur.execute(sql, args)
        conn.commit()
        close_conn(conn, cur)
        return True
    except Exception as e:
        print("token insert except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False


#查找记录是否存在

def select_record(sql, args):
    conn, cur = create_conn()
    try:
        result = cur.execute(sql, args)
        conn.commit()
        close_conn(conn, cur)
        if result==0:
            return True
        else:
            return False
    except Exception as e:
        print("user select except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False




def record_insert(sql, args):
    conn, cur = create_conn()
    try:
        cur.execute(sql, args)
        conn.commit()
        close_conn(conn, cur)
        return True
    except Exception as e:
        print("token insert except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False


def user_insert(sql, args):
    conn, cur = create_conn()
    try:
        result = cur.execute(sql, args)
        conn.commit()
        close_conn(conn, cur)
        return True
    except Exception as e:
        print("user insert except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False


def select_user_login(sql, args):
    conn, cur = create_conn()
    try:
        cur.execute(sql, args)
        conn.commit()
        close_conn(conn, cur)
        res = cur.fetchall()
        for r in res:
            username = r['userName']
            email = r['email']
            usertype = r['userType']
            print("select_user_login=>", username, email, usertype)
        if len(res) == 0:
            return ''
        return username, email, usertype
    except Exception as e:
        print("user select except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False

def select_get_user(sql, args):
    conn, cur = create_conn()
    try:
        result = cur.execute(sql, args)
        conn.commit()
        close_conn(conn, cur)
        return True if result == 0 else False
    except Exception as e:
        print("user select except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False

def select_get_user_info(args):
    conn, cur = create_conn()
    try:
        cur.execute("select * from user where userName = %s", args)
        conn.commit()
        close_conn(conn, cur)
        res = cur.fetchall()
        for r in res:
            id = r['id']
            username = r['userName']
            email = r['email']
            usertype = r['userType']
            print("select_get_user_info=>", username, email, usertype)
        if len(res) == 0:
            return ''

        return {
            "id": id,
            "username": username,
            "email": email,
            "usertype": usertype,
        }
    except Exception as e:
        print("user select except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False

def select_get_userid(sql, args):
    conn, cur = create_conn()
    try:
        result = cur.execute(sql, args)
        data = cur.fetchone()
        conn.commit()
        close_conn(conn, cur)
        return data['id']
    except Exception as e:
        print("user select except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False

def select_records():
    conn, cur = create_conn()
    try:
        cur.execute("select * from record  order by no desc")
        result = cur.fetchall()
        conn.commit()
        close_conn(conn, cur)
        return result
    except Exception as e:
        print("records select except")
        conn.rollback()
        close_conn(conn, cur)
        return False

def select_records_assigned_to_user(userId):
    conn, cur = create_conn()
    try:
        cur.execute(
            "select no, assignment.score, comment from record right outer join assignment on record_id = no where user_id = %s order by no desc",
            userId
        )
        result = cur.fetchall()
        conn.commit()
        close_conn(conn, cur)
        return result
    except Exception as e:
        print("records select except")
        conn.rollback()
        close_conn(conn, cur)
        return False


def encode_(str):
    MD5 = hashlib.md5()
    MD5.update(str.encode(encoding='utf-8'))
    print("加密后：", MD5.hexdigest())
    return MD5.hexdigest()


# sql = "select * from user where userName=%s "
# q = "🍺🐷"
# res = select_all(sql, q)
# print(res)
def update_token(sql, args):
    conn, cur = create_conn()
    try:
        cur.execute(sql, args)
        conn.commit()
        close_conn(conn, cur)
        return True
    except Exception as e:
        print("user_token update except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False

def user_usertype_update(sql, args):
    conn, cur = create_conn()
    try:
        cur.execute(sql, args)
        conn.commit()
        close_conn(conn, cur)
        return True
    except Exception as e:
        print("user insert except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False

def select_email(sql, args):
    conn, cur = create_conn()
    try:
        cur.execute(sql, args)
        conn.commit()
        close_conn(conn, cur)
        res = cur.fetchall()
        for r in res:
            email = r['email']
        if len(res) == 0:
            return ''
        return email
    except Exception as e:
        print("user select except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False

def select_path_by_no(args):
    conn, cur = create_conn()
    try:
        sql = "select file_path from record where no = %s"
        cur.execute(sql, args)
        conn.commit()
        close_conn(conn, cur)
        res = cur.fetchall()
        for r in res:
            path = r['file_path']
        if len(res) == 0:
            return ''
        return  path

    except Exception as e:
        print("select path except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False



def update_pwd(sql, args):
    conn, cur = create_conn()
    try:
        result = cur.execute(sql, args)
        conn.commit()
        close_conn(conn, cur)
        if result == 1:
            return True
        return False
    except Exception as e:
        print("user select except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False

def select_users_by_type(args):
    conn, cur = create_conn()
    try:
        cur.execute("select * from user where userType = %s", args)
        result = cur.fetchall()
        conn.commit()
        close_conn(conn, cur)
        return result
    except Exception as e:
        print("users select except")
        conn.rollback()
        close_conn(conn, cur)
        return False

def assign_record_to_user(recordId, userId):
    conn, cur = create_conn()
    try:
        cur.execute(
            "insert into assignment (record_id, user_id) values (%s, %s)",
            [recordId, userId]
        )
        conn.commit()
        close_conn(conn, cur)
        return True
    except Exception as e:
        print("assignment insert except")
        conn.rollback()
        close_conn(conn, cur)
        return False

def deassign_record_to_user(recordId, userId):
    conn, cur = create_conn()
    try:
        cur.execute(
            "delete from assignment where record_id = %s and user_id = %s",
            [recordId, userId]
        )
        conn.commit()
        close_conn(conn, cur)
        return True
    except Exception as e:
        print("assignment delete except")
        conn.rollback()
        close_conn(conn, cur)
        return False

def select_assigned_users_by_record(args):
    conn, cur = create_conn()
    try:
        cur.execute("select * from assignment where record_id = %s", args)
        result = cur.fetchall()
        conn.commit()
        close_conn(conn, cur)
        return result
    except Exception as e:
        print("assignment select except")
        conn.rollback()
        close_conn(conn, cur)
        return False

def comment_record(recordId, userId, score, comment):
    conn, cur = create_conn()
    try:
        cur.execute(
            "update assignment set score = %s, comment = %s where record_id = %s and user_id = %s",
            [score, comment, recordId, userId]
        )
        conn.commit()
        close_conn(conn, cur)
        return True
    except Exception as e:
        print("comment record except")
        conn.rollback()
        close_conn(conn, cur)
        return False

def select_not_commented(userId):
    conn, cur = create_conn()
    try:
        cur.execute(
            "select count(*) from assignment where user_id = %s and score is null and comment is null",
            [userId]
        )
        result = cur.fetchall()
        conn.commit()
        close_conn(conn, cur)
        return result
    except Exception as e:
        print("not commented select except")
        conn.rollback()
        close_conn(conn, cur)
        return False

def apply_consultant(userId, form):
    conn, cur = create_conn()
    try:
        cur.execute(
            "insert into apply_consultant (user_id, form_json, status) values (%s, %s, 0)",
            [userId, form]
        )
        conn.commit()
        close_conn(conn, cur)
        return True
    except Exception as e:
        print("apply consultant insert except")
        conn.rollback()
        close_conn(conn, cur)
        return False

def specify_bps(bps):
    conn, cur = create_conn()
    try:
        cur.execute("update record set isWaiting=0")
        format_strings = ','.join(['%s'] * len(bps))
        cur.execute(
            "update record set isWaiting=1 where no in (%s)" % format_strings,
            tuple(bps)
        )
        conn.commit()
        close_conn(conn, cur)
        return True
    except Exception as e:
        print("specify bp except")
        conn.rollback()
        close_conn(conn, cur)
        return False

def get_consultant_applications():
    conn, cur = create_conn()
    try:
        cur.execute(
            "select apply_consultant.id as id, user_id, userName, status from apply_consultant left outer join user on user.id = user_id order by apply_consultant.id desc"
        )
        result = cur.fetchall()
        conn.commit()
        close_conn(conn, cur)
        return result
    except Exception as e:
        print("select consultant applications except")
        conn.rollback()
        close_conn(conn, cur)
        return False

def get_consultant_application_by_id(id):
    conn, cur = create_conn()
    try:
        cur.execute(
            "select apply_consultant.id as id, form_json, user_id, userName, status from apply_consultant left outer join user on user.id = user_id where apply_consultant.id = %s",
            [id]
        )
        result = cur.fetchall()
        conn.commit()
        close_conn(conn, cur)
        return result
    except Exception as e:
        print("select consultant applications except")
        conn.rollback()
        close_conn(conn, cur)
        return False

def pass_consultant_applications(id):
    conn, cur = create_conn()
    try:
        cur.execute(
            "update apply_consultant set status=2 where id = %s",
            [id]
        )
        cur.execute(
            "update user set userType=2 where id in (select user_id from apply_consultant where id = %s)",
            [id]
        )
        conn.commit()
        close_conn(conn, cur)
        return True
    except Exception as e:
        print("update consultant applications except")
        conn.rollback()
        close_conn(conn, cur)
        return False

def reject_consultant_applications(id):
    conn, cur = create_conn()
    try:
        cur.execute(
            "update apply_consultant set status=1 where id = %s",
            [id]
        )
        cur.execute(
            "update user set userType=1 where id in (select user_id from apply_consultant where id = %s)",
            [id]
        )
        conn.commit()
        close_conn(conn, cur)
        return True
    except Exception as e:
        print("update consultant applications except")
        conn.rollback()
        close_conn(conn, cur)
        return False

def select_records_assigned_to_user_as_admin(userId):
    conn, cur = create_conn()
    try:
        cur.execute(
            "select no, record.score as ai_score, assignment.score, comment from record right outer join assignment on record_id = no where user_id = %s order by no desc",
            userId
        )
        result = cur.fetchall()
        conn.commit()
        close_conn(conn, cur)
        return result
    except Exception as e:
        print("records select except")
        conn.rollback()
        close_conn(conn, cur)
        return False
