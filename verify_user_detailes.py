from fastapi import APIRouter
from connection import execute_sql,execute_commit_sql;

cache = {}
router = APIRouter()


def is_exist(sql):
    return execute_sql(sql)
    

@router.post('/login')
def login(params:dict):
    print(params)
    sql = f"SELECT user, status FROM chat.users WHERE user = '{params['username']}'"
    print(sql)
    check_is_exist = is_exist(sql)
    print(check_is_exist)
    if len(check_is_exist) > 0:
        if  check_is_exist[0]['status'] == 1:
            ## i am in return user already in
            print("already connected")
            return {'success': False}
        else:
            ## update cache + update db user dtatus to connect
            sql = f"UPDATE chat.users SET status = 1 WHERE user = '{params['username']}'"
            print(sql)

            execute_commit_sql(sql)
            cache[params['username']]= 1
            return {'success': True}
        
    else:
        sql = """INSERT INTO chat.users (username, type) VALUES (params['username'], 'normal'))"""
        print(sql)
        execute_commit_sql(sql)
        cache[params['username']] = 1
        return {'success': True}

