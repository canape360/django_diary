# myapp/migrations/0002_fix_missing_user_id.py
from django.db import migrations

def add_user_id_if_missing(apps, schema_editor):
    table = "myapp_diary"
    vendor = schema_editor.connection.vendor  # "postgresql" / "sqlite" / ...

    with schema_editor.connection.cursor() as cursor:
        if vendor == "postgresql":
            # Postgres: information_schema で列有無チェック
            cursor.execute(
                """
                SELECT 1
                FROM information_schema.columns
                WHERE table_name = %s AND column_name = 'user_id'
                """,
                [table],
            )
            exists = cursor.fetchone() is not None

            if exists:
                return

            cursor.execute(f'ALTER TABLE "{table}" ADD COLUMN "user_id" integer NULL;')

            cursor.execute(
                f"""
                DO $$
                BEGIN
                    ALTER TABLE "{table}"
                    ADD CONSTRAINT "myapp_diary_user_id_fk"
                    FOREIGN KEY ("user_id")
                    REFERENCES "auth_user" ("id")
                    DEFERRABLE INITIALLY DEFERRED;
                EXCEPTION WHEN duplicate_object THEN
                    NULL;
                END $$;
                """
            )
            cursor.execute(
                f'CREATE INDEX IF NOT EXISTS "myapp_diary_user_id_idx" ON "{table}" ("user_id");'
            )

        elif vendor == "sqlite":
            # SQLite: PRAGMA table_info で列有無チェック
            cursor.execute(f'PRAGMA table_info("{table}");')
            cols = [row[1] for row in cursor.fetchall()]  # row[1] = column name
            if "user_id" in cols:
                return
            # SQLiteは ADD COLUMN はできる（FK制約やindexは簡易）
            cursor.execute(f'ALTER TABLE "{table}" ADD COLUMN "user_id" integer NULL;')
            cursor.execute(f'CREATE INDEX IF NOT EXISTS "myapp_diary_user_id_idx" ON "{table}" ("user_id");')

        else:
            # 他DBは今は何もしない（必要なら追加）
            return

class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_user_id_if_missing, migrations.RunPython.noop),
    ]
