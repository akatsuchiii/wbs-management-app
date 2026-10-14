from pathlib import Path
import psycopg

# 実行するSQLファイルのパス
sql_file = Path(__file__).parent / "sql" / "001_create_users.sql"

# SQLファイルを読み込む
sql = sql_file.read_text(encoding="utf-8")

try:
    # PostgreSQLに接続
    with psycopg.connect(connect_timeout=10) as conn:

        # SQLを実行
        with conn.cursor() as cur:
            cur.execute(sql)

    print("usersテーブルの作成に成功しました！")

except psycopg.Error as e:
    print("テーブルの作成に失敗しました。")
    print("エラー:", e)