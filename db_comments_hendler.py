from fastapi import APIRouter
from connection import execute_sql,execute_commit_sql;

router = APIRouter()


def is_superuser(sql):
    return execute_sql(sql)


@router.post('/new_comment')
def post_new_comment(params:dict):
    sql = """UPDATE chat.comment SET comment"""
    try:
        execute_commit_sql(sql)
    except Exception as error:
        print(str(error))

@router.post('/delete_comment')
def delete_comment(params:dict):
    sql = """DELETE comment FROM chat.comment WHERE userID = params['userID'] AND msgID = params['msgID']"""
    try:
        execute_commit_sql(sql)
    except Exception as error:
        print(str(error))