# myapp/migrations/0003_drop_not_null_person_id.py
from django.db import migrations

def fix_person_id_nullable(apps, schema_editor):
    table = "myapp_diary"
    vendor = schema_editor.connection.vendor  # "postgresql" / "sqlite" / ...

    with schema_editor.connection.cursor() as cursor:
        if vendor == "postgresql":
            # person_id 列が存在するか確認（存在しないなら何もしない）
            cursor.execute(
                """
                SELECT 1
                FROM information_schema.columns
                WHERE table_name = %s AND column_name = 'person_id'
                """,
                [table],
            )
            exists = cursor.fetchone() is not None
            if not exists:
                return

            # NOT NULL 制約を外す（NULL許可にする）
            cursor.execute(f'ALTER TABLE "{table}" ALTER COLUMN "person_id" DROP NOT NULL;')

        elif vendor == "sqlite":
            # SQLite では NOT NULL を DROP する ALTER ができないため、
            # ローカルで person_id が無い（通常）なら何もしない。
            cursor.execute(f'PRAGMA table_info("{table}");')
            cols = [row[1] for row in cursor.fetchall()]
            if "person_id" in cols:
                # もし SQLite に person_id があり NOT NULL なら、テーブル再構築が必要。
                # ここでは壊さないため何もしない。
                return

        else:
            return

class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0002_fix_missing_user_id"),
    ]

    operations = [
        migrations.RunPython(fix_person_id_nullable, migrations.RunPython.noop),
    ]
