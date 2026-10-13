from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI(title="Wibby")
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTMLテンプレートの保存場所を指定
templates = Jinja2Templates(directory="templates")

#プロジェクト登録時に受け取るデータの形
class ProjectCreate(BaseModel):
    name:str
    description:str


projects = [
    {
        "id": 1,
        "name": "Webサイト制作",
        "description": "会社紹介用のWebサイトを制作するプロジェクト",
    },
    {
        "id": 2,
        "name": "WBS管理アプリ開発",
        "description": "タスクと進捗を管理するアプリを開発するプロジェクト",
    },
]

# ログインユーザー情報
loginUser = {
    "username":"admin",
    "password": "admin",
}


@app.post("/projects")
def create_project(project: ProjectCreate):

    new_project = {
        "id":len(projects) + 1,
        "name":project.name,
        "description":project.description
    }

    projects.append(new_project)

    return new_project

@app.get("/projects/{project_id}")
def get_project(project_id: int):

    for project in projects:
        if project_id == project["id"]:
            return project

    raise HTTPException(
        status_code=404,
        detail="Project not found"
    )
    
# ログイン画面を表示
@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )
    
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    regUserNm = loginUser["username"]
    regUserPw = loginUser["password"]
    
    if username == regUserNm and password == regUserPw:
        return RedirectResponse(
            url="/home",
            status_code=303
        )
    else:
        raise HTTPException(
            status_code=404,
            detail="Invalid username or password"
        )

@app.get("/home")
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html"
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to Wibby!"}