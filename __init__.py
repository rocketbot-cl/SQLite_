import os
import sys
global cursor
global conn
global hostname
global username
global password
global database

base_path = tmp_global_obj["basepath"]
cur_path = base_path + 'modules' + os.sep + 'PostgreSQL' + os.sep + 'libs' + os.sep
sys.path.append(cur_path)
print(cur_path)

import psycopg2

module = GetParams('module')

if module == "connect":
    hostname = GetParams('hostname')
    username = GetParams('username')
    password = GetParams('password')
    database = GetParams('database')
    var_ = GetParams('var_')
    print(hostname,username,password,database)

    status = False

    try:
        conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        cursor = conn.cursor()
        status = True
    except:
        PrintException()


    SetVar(var_,status)


if module == "execute":
    query_ = GetParams('query_')
    result = []
    var_ = GetParams('var_')

    try:
        conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        cursor = conn.cursor()
    except:
        PrintException()

    try:
        query = query_
        cursor.execute(query)

        if "select" in query.lower():


            col = [d[0] for d in cursor.description]
            print('COL', col)

            rows = cursor.fetchall()

            for row in rows:
                # print(row)
                ob_ = {}
                t = 0
                for r in row:
                    ob_[col[t]] = str(r) + ""
                    t = t + 1
                result.append(ob_)

        else:
            conn.commit()
            result = "True"
            #result = cur.rowcount

        # print(result)
        conn.close()
        SetVar(var_, result)
    except Exception as e:
        PrintException()
        raise e