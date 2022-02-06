
import mysql.connector

from fastapi_utils.tasks import repeat_every
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html

dbpool = None
cnx = None
def connect():
    global dbpool 
    global cnx

    try:
        cnx = mysql.connector.connect(host='localhost',port="3306",user='root',password='root',database='chat')
        dbpool = cnx.cursor(dictionary=True)
        # cnx.close()
    except mysql.connector.Error as err:
        print(err)

def execute_sql(sql):
    print(sql)
    global dbpool 
    global cnx
    try:

        dbpool.execute(sql)
        result =  dbpool.fetchall()
        return result
    except Exception as error:
        print(str(error) + sql)

def execute_commit_sql(sql):
    print(sql)
    global dbpool 
    global cnx

    try:
        dbpool.execute(sql)
        cnx.commit()
        result =  dbpool.fetchall()
        return result
    except Exception as error:
        print(str(error) + sql)
   