from flaskr.database import db
from flaskr import create_app
from sqlalchemy.sql import text

app = create_app()
app.app_context().push() # required for interacting with the SQLAlchemy db object

# List of area names
areas = [
    "General Discussion",
    "Rules & Mechanics",
    "Strategy & Tactics",
    "Game Analysis",
    "Tournaments & Events",
    "Similar Games",
    "Introductions",
    "Off-Topic",
    "Feedback & Suggestions"
]

for area_name in areas:
    # Construct the SQL query
    sql = text("""
    INSERT INTO areas (name, is_secret)
    VALUES (:name, :is_secret)
    ON CONFLICT (name) DO NOTHING;
    """)
    
    # Execute the SQL query
    db.session.execute(sql, {"name": area_name, "is_secret": False})
    
# Commit the transaction
db.session.commit()
