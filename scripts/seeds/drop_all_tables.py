from source.app import create_app
from source.app.settings.definitions_settings import db

app = create_app()

with app.app_context():
    try:
        db.drop_all()
        print("All tables have been successfully deleted!")
    except Exception as e:
        print(f"Error deleting tables: {e}")