import psycopg
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, HTTPException
from pathlib import Path


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
