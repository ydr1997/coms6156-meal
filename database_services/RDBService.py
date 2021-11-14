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
        for k,v in template.items():
            terms.append(k + "=%s")
            args.append(v)

        clause = " where " +  " AND ".join(terms)


    return clause, args


def find_by_template(db_schema, table_name, template, field_list):

    wc,args = _get_where_clause_args(template)

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " " + wc
    res = cur.execute(sql, args=args)
    res = cur.fetchall()

    conn.close()

    return res


def get_mealsfromid(meals_id):

    conn = _get_db_connection()
    cur = conn.cursor()

    mm =  "meal_information"
    # print(meals_id)

    # sql = "select * from " + "ec2_lookmeal" + "." + "meal_information" + "WHERE ID = (" + meals_id

    sql = "select * from " + "ec2_lookmeal" + "." + mm + " " + "where id = " + meals_id

    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
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

def add_meals():
    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "INSERT INTO " + "ec2_lookmeal" + "." + "meal_information" + " (id,creator,location,restaurant,max_number,current_number) VALUES (%s,%s, %s, %s, %s, %s)"
    # sql = "Insert into " + db_schema + "." + table_name + " (ID, firstName, lastName, email, addressID) VALUES (" + id + ",'" + firstName + "','" + lastName + "','" + email + "'," + addressID + ")"
    print("SQL Statement = " + cur.mogrify(sql, None))




    res = cur.execute(sql,(11111, 'try', '11111st', 'temprestaurant', 1000, 555))
    res = cur.fetchall()

    conn.commit()

    conn.close()

    return res