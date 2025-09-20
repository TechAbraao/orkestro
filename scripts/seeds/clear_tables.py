from source.app import create_app
from source.app.settings.definitions_settings import db

app = create_app()

with app.app_context():
    connection = db.engine.connect()
    trans = connection.begin()
    try:
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            connection.execute(table.delete())
        trans.commit()
        print("All tables have been cleaned successfully.")
    except Exception as e:
        trans.rollback()
        print(f"Error clearing bank: {e}")
    finally:
        connection.close()