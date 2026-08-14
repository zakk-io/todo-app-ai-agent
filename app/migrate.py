from sqlalchemy import text

from app.database import engine


def run_migrations():
    with engine.begin() as conn:
        conn.execute(
            text(
                "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS created_at "
                "TIMESTAMP WITH TIME ZONE DEFAULT now()"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS updated_at "
                "TIMESTAMP WITH TIME ZONE DEFAULT now()"
            )
        )