from fastapi import FastAPI,Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from api.users.users import usersRouter

app = FastAPI(title="User Api", description="User Api Presentation")
templates = Jinja2Templates(directory="templates/")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(usersRouter, prefix="/users", tags=["Users"])


@app.get("/", tags=["Home Page"], summary="Home Page link")
async def home_page(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


