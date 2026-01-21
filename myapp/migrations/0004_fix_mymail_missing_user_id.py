# myapp/migrations/0004_fix_mymail_missing_user_id.py
from django.db import migrations

def add_mymail_user_id_if_missing(apps, schema_editor):
    table = "myapp_mymail"
    vendor = schema_editor.connection.vendor

    with schema_editor.connection.cursor() as cursor:
        if vendor == "postgresql":
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

            # まず列を追加（モデルは null=True なので NULL許可でOK）
            cursor.execute(f'ALTER TABLE "{table}" ADD COLUMN "user_id" integer NULL;')

            # FK制約（auth_user.id）: 同名があれば無視
            cursor.execute(
                f"""
                DO $$
                BEGIN
                    ALTER TABLE "{table}"
                    ADD CONSTRAINT "myapp_mymail_user_id_fk"
                    FOREIGN KEY ("user_id")
                    REFERENCES "auth_user" ("id")
                    DEFERRABLE INITIALLY DEFERRED;
                EXCEPTION WHEN duplicate_object THEN
                    NULL;
                END $$;
                """
            )

            cursor.execute(
                f'CREATE INDEX IF NOT EXISTS "myapp_mymail_user_id_idx" ON "{table}" ("user_id");'
            )

        elif vendor == "sqlite":
            cursor.execute(f'PRAGMA table_info("{table}");')
            cols = [row[1] for row in cursor.fetchall()]
            if "user_id" in cols:
                return

            cursor.execute(f'ALTER TABLE "{table}" ADD COLUMN "user_id" integer NULL;')
            cursor.execute(
                f'CREATE INDEX IF NOT EXISTS "myapp_mymail_user_id_idx" ON "{table}" ("user_id");'
            )

        else:
            return

class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0003_drop_not_null_person_id"),
    ]

    operations = [
        migrations.RunPython(add_mymail_user_id_if_missing, migrations.RunPython.noop),
    ]
