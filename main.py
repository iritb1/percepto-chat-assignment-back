
import uvicorn
import logging
from connection import connect;
from fastapi import FastAPI, Request, HTTPException, WebSocket   
from fastapi_utils.tasks import repeat_every
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html


logger = logging.getLogger("werkzug")
logger.setLevel(logging.DEBUG)

app = FastAPI(title="percepto", description="chat app",
              version="1.0.6", docs_url="/doc", redoc_url="/redoc")
#
# Load the app after build
STATIC_FOLDER = 'front/dist'
# UPLOAD_FOLDER = 'front\\dist\\attach'

# Import Managers
import db_comments_hendler
import verify_user_detailes

# Add Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
origins = [
    "*",
    "http://localhost:3002",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Install Routers
app.include_router(db_comments_hendler.router,prefix="/comment", tags=["comment"])
app.include_router(verify_user_detailes.router,prefix="/user", tags=["user"])

connect()
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



# Offline Serving of API Docs
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/html/swagger-ui-bundle.js",
        swagger_css_url="/html/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/html/redoc.standalone.js",
    )

##
#   Background Process
##
counter = 0
@app.on_event("startup")
@repeat_every(seconds=300, logger=logger, wait_first=True)
def periodic():
    global counter
    print('background worker called ' + str(counter))
    counter += 1


# Startup
@app.on_event("startup")
def startup():
    print('running startup')


# Shutdown
@app.on_event("shutdown")
def shutdown():
    print('shutting down')

app.mount('/', StaticFiles(directory=STATIC_FOLDER), name=STATIC_FOLDER)
templates = Jinja2Templates(directory=STATIC_FOLDER)

if __name__=='__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)



