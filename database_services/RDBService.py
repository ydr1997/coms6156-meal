import pymysql
import json
import logging

import middleware.context as context

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _get_db_connection():
    db_connect_info = context.get_db_info()

    logger.info("RDBService._get_db_connection:")
    logger.info("\t HOST = " + db_connect_info['host'])

    db_info = context.get_db_info()
    db_connection = pymysql.connect(
        **db_info
    )
    return db_connection


def get_by_prefix(db_schema, table_name, column_name, value_prefix):
    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " where " + \
          column_name + " like " + "'" + value_prefix + "%'"
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()

    conn.close()

    return res


def _get_where_clause_args(template):
    terms = []
    args = []
    clause = None

    if template is None or template == {}:
        clause = ""
        args = None
    else:
        for k, v in template.items():
            terms.append(k + "=%s")
            args.append(v)

        clause = " where " + " AND ".join(terms)

    return clause, args


def find_by_template(db_schema, table_name, template, field_list):
    wc, args = _get_where_clause_args(template)

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " " + wc
    res = cur.execute(sql, args=args)
    res = cur.fetchall()

    conn.close()

    return res


def get_all( ):

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + "ec2_lookmeal" + "." + "make_team"

    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()

    conn.close()

    return res

def meals_delete_id(meals_id):
    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "Delete from ec2_lookmeal.meal_information where id=" + meals_id

    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()
    conn.commit()
    conn.close()

    return res


def add_meals(id, creator, location, restaurant, max_number, current_number):       #??????????????????
    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "INSERT INTO " + "ec2_lookmeal" + "." + "meal_information" + " (id,creator,location,restaurant,max_number,current_number) VALUES (%s,%s, %s, %s, %s, %s)"

    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql,(id, creator, location, restaurant, max_number, current_number))
    res = cur.fetchall()

    conn.commit()
    conn.close()

    return res


def meals_modificate_add(meals_id, participant):       #??????????????????,???meals_information?????????meals_id>???current_number - 1?????????make_team????????????<meals_id> <participant>???????????????
    conn = _get_db_connection()
    cur = conn.cursor()

    sql1 = "UPDATE ec2_lookmeal.meal_information SET current_number=current_number - 1 WHERE id=" + meals_id
    print("SQL Statement = " + cur.mogrify(sql1, None))
    cur.execute(sql1)
    cur.fetchall()

    sql = "INSERT INTO " + "ec2_lookmeal" + "." + "make_team" + "(meals_id, participant) VALUES(%s, %s)"
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql, (meals_id, participant))
    res = cur.fetchall()

    conn.commit()
    conn.close()

    return res

# def meals_modificate_delete(meals_id, participant):   #########delete sql???????????????????????????
#     conn = _get_db_connection()
#     cur = conn.cursor()
#
#     sql1 = "UPDATE ec2_lookmeal.meal_information SET current_number=current_number + 1 WHERE id=" + meals_id
#     print("SQL Statement = " + cur.mogrify(sql1, None))
#     cur.execute(sql1)
#     cur.fetchall()
#
#     sql = "Delete from ec2_lookmeal.make_team where id=" + meals_id+ " and participant=" + participant VALUES (%s)
#     # sql = "INSERT INTO " + "ec2_lookmeal" + "." + "make_team" + "(meals_id, participant) VALUES(%s, %s)"
#     print("SQL Statement = " + cur.mogrify(sql, None))
#
#
#     res = cur.execute(sql,(participant))
#     res = cur.fetchall()
#     conn.commit()
#     conn.close()
#
#     return res

# def meals_delete_id(meals_id):
#     conn = _get_db_connection()
#     cur = conn.cursor()
#
#     sql = "Delete from ec2_lookmeal.meal_information where id=" + meals_id
#
#     print("SQL Statement = " + cur.mogrify(sql, None))
#
#     res = cur.execute(sql)
#     res = cur.fetchall()
#     conn.commit()
#     conn.close()
#
#     return res


# def meals_modificate_delete(meals_id, participant):   #########delete??????????????????
#     conn = _get_db_connection()
#     cur = conn.cursor()
#
#     sql1 = "UPDATE ec2_lookmeal.meal_information SET current_number=current_number + 1 WHERE id=" + meals_id
#     print("SQL Statement = " + cur.mogrify(sql1, None))
#     cur.execute(sql1)
#     cur.fetchall()
#
#     sql = "Delete from ec2_lookmeal.make_team where id=" +"meals_id VALUES(%s)" +" "+ "and participant=" + "participant VALUES(%s)"
#
#     print("SQL Statement = " + cur.mogrify(sql, None))
#
#     res = cur.execute(sql, ( meals_id, participant))
#     res = cur.fetchall()
#
#     conn.commit()
#     conn.close()
#
#     return res


def get_maketeam(db_schema, table_name):
    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()
    print(res)

    conn.close()

    return res

def get_mealinformation(db_schema, table_name):
    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()
    print(res)

    conn.close()

    return res


def get_mealsfromid(db_schema, table_name, meals_id):
    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " where id = " + meals_id
    print(sql)
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()
    print(res)

    conn.close()

    return res

def participant_take_meal(db_schema, table_name, participant_id):
    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " where participant = " + participant_id
    print(sql)
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()
    print(res)

    conn.close()

    return res

def creator_create_meal(db_schema, table_name, creator_id):
    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " where creator = " + creator_id
    print(sql)
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()
    print(res)

    conn.close()

    return res
