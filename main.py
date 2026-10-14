
import os

import psycopg
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pwdlib import PasswordHash
from starlette.middleware.sessions import SessionMiddleware

from routers.projects import router as projects_router


# FastAPIアプリの作成
app = FastAPI(title="Wibby")

# セッション管理
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ["SESSION_SECRET_KEY"],
    same_site="lax",
    https_only=False,  # ローカル開発用
)

# ルーターの登録
app.include_router(projects_router)

# 静的ファイル・HTMLテンプレートの設定
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# パスワード照合用
password_hash = PasswordHash.recommended()


# ルート画面
@app.get("/")
def read_root():
    return RedirectResponse(url="/login")


# ログイン画面
@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
    )


# ログイン認証
@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    try:
        with psycopg.connect(connect_timeout=10) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, password_hash
                    FROM users
                    WHERE username = %s
                      AND deleted_at IS NULL
                    """,
                    (username,),
                )
                user = cur.fetchone()

    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="Database connection error",
        )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    user_id, stored_hash = user

    if not password_hash.verify(password, stored_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    request.session["user_id"] = user_id

    return RedirectResponse(url="/home", status_code=303)


# ホーム画面
@app.get("/home")
def dashboard(request: Request):
    if "user_id" not in request.session:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="home.html",
    )
