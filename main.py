from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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


@app.get("/projects")
def get_projects():
    return projects

@app.post("/projects")
def create_project(project: ProjectCreate):

    new_project = {
        "id":len(projects) + 1,
        "name":project.name,
        "description":project.description
    }

    projects.append(new_project)

    return new_project


@app.get("/")
def read_root():
    return{"message":"WBS管理アプリ"}