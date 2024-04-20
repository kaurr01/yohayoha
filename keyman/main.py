from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud



models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

user_credits = {}  # In-memory storage for user credits


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/signup/")
async def signup(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(username, db)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Create user and store in database
    new_user = crud.create_user(username, password, db)

    # Assign credits to the new user (in memory)
    user_credits[new_user.username] = 3

    return templates.TemplateResponse("signup_success.html", {"request": request, "username": new_user.username, "credits": user_credits.get(new_user.username, 0)})








@app.get("/signup/", response_class=HTMLResponse)
async def show_signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/login/")
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(username, db)
    if not db_user or db_user.password != password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return templates.TemplateResponse("login_success.html", {"request": request, "username": username})


@app.get("/login/", response_class=HTMLResponse)
async def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

