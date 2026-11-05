import psycopg
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, HTTPException
from pathlib import Path
from pydantic import BaseModel
from datetime import date

# 登録機能用
class ProjectCreate(BaseModel):
    name: str
    summary: str | None = None
    str_date: date | None = None
    end_date: date | None = None
    status: str

# 削除機能用
class ProjectDelete(BaseModel):
    projectId: list[int]


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/projects")
def projects_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="projects.html",
    )

@router.get("/api/projects")
def get_projects(request: Request):
    if "user_id" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )

    with psycopg.connect(connect_timeout=10) as conn:
        with conn.cursor() as cur:
            sql_path = Path(__file__).resolve().parent.parent / "sql" / "get_projects.sql"
            sql = sql_path.read_text(encoding="utf-8")
            cur.execute(sql)

            projects = cur.fetchall()
            result = []
            for project in projects:
                result.append({
                    "id":project[0],
                    "name":project[1],
                    "start_date":project[2],
                    "end_date":project[3],
                    "status":project[4]
                })

    return result


@router.get("/api/projects/columns")
def get_project_columns(request:Request):
    if "user_id"not in request.session:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )
    with psycopg.connect(connect_timeout=10) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = 'projects'
                ORDER BY ordinal_position
            """)

            columns = cur.fetchall()

    result = []

    for column in columns:
        result.append(column[0])

    return result


@router.post("/api/projects", status_code=201)
def create_project(project: ProjectCreate, request: Request):

    # ログイン状態の確認
    user_id = request.session.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    # SQLファイルの読み込み
    sql_path = Path(__file__).resolve().parent.parent / "sql" / "regist_project.sql"
    sql = sql_path.read_text(encoding="utf-8")

    # 登録するデータを作成
    params = {
        "name": project.name,
        "description": project.summary,
        "start_date": project.str_date,
        "end_date": project.end_date,
        "status": project.status,
        "created_by": user_id
    }

    # PostgreSQLへ登録
    with psycopg.connect(connect_timeout=10) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)

            # 登録されたプロジェクトIDを取得
            project_id = cur.fetchone()[0]

    return {
        "id": project_id,
        "message": "Project created successfully"
    }

# 1件のみ削除関数
# @router.delete("/api/projects/{project_id}")
# def delete_project(project_id: int, request: Request):

#     # ログインユーザーを取得
#     user_id = request.session.get("user_id")

#     if user_id is None:
#         raise HTTPException(
#             status_code=401,
#             detail="Not authenticated"
#         )

#     # SQLファイルを読み込み
#     sql_path = (
#         Path(__file__).resolve().parent.parent
#         / "sql"
#         / "delete_project.sql"
#     )
#     sql = sql_path.read_text(encoding="utf-8")

#     # PostgreSQLから削除
#     with psycopg.connect(connect_timeout=10) as conn:
#         with conn.cursor() as cur:
#             cur.execute(sql, {
#                 "project_id": project_id,
#                 "user_id": user_id
#             })

#             deleted_project = cur.fetchone()

#     # 削除対象が存在しない場合
#     if deleted_project is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Project not found"
#         )

#     return {
#         "id": deleted_project[0],
#         "message": "Project deleted successfully"
#     }


# 複数選択にも対応した削除関数
@router.delete("/api/projects/bulk")
def delete_projects(projects: ProjectDelete, request: Request):
    user_id = request.session.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    project_ids = projects.projectId

    # 配列が0件の場合
    if len(project_ids) == 0:
        raise HTTPException(
            status_code=400,
            detail="削除対象が指定されていません"
        )
    # 重複IDチェック
    if len(project_ids) != len(set(project_ids)):
        raise HTTPException(
            status_code=400,
            detail="重複したIDが選択されています。"
        )

    # SQLファイルの読み込み
    sql_path = Path(__file__).resolve().parent.parent / "sql" / "delete_project.sql"
    sql = sql_path.read_text(encoding="utf-8")

    # パラメータ設定
    params ={
        "project_ids": project_ids,
        "user_id": user_id
    }

    with psycopg.connect(connect_timeout=10) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            deleted_rows = cur.fetchall()

            if len(project_ids) != len(deleted_rows):
                raise HTTPException(
                    status_code=409,
                    detail="削除対象の一部が存在しないか、削除権限がありません"
                )

    deleted_ids = [row[0] for row in deleted_rows]
    return {
            "deleted_ids": deleted_ids
        }