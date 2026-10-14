import getpass

import psycopg
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

# ユーザー情報を入力
username = input("ユーザー名: ")
display_name = input("表示名: ")
password = getpass.getpass("パスワード: ")

# パスワードをハッシュ化
hashed_password = password_hash.hash(password)

try:
    with psycopg.connect(connect_timeout=10) as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO users (
                    username,
                    display_name,
                    password_hash
                )
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (username, display_name, hashed_password)
            )

            user_id = cur.fetchone()[0]

    print("ユーザー登録成功！")
    print("ユーザーID:", user_id)

except psycopg.errors.UniqueViolation:
    print("そのユーザー名は既に登録されています。")

except psycopg.Error as e:
    print("ユーザー登録失敗")
    print("エラー種別:", type(e).__name__)