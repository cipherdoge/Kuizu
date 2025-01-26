import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Score  # import your models

# Path to the database file in the instance folder
db_file = os.path.join('/home/ritvik/quiz_master_v2/Kuizu/backend/instance', 'app.db')

# Create an engine that will connect to the SQLite database
engine = create_engine(f'sqlite:///{db_file}')

# Bind SQLAlchemy session to this engine
Session = sessionmaker(bind=engine)
session = Session()
"""
# Update user_id in the existing Score records
try:
    # Assuming you want to change all scores for user_id=1 to user_id=2
    old_user_id = 1
    new_user_id = 2

    # Query for all Score records with the old user_id
    scores_to_update = session.query(Score).filter(Score.user_id == old_user_id).all()

    if scores_to_update:
        for score in scores_to_update:
            score.user_id = new_user_id

        # Commit the changes to the database
        session.commit()
        print(f"Successfully updated {len(scores_to_update)} scores to user_id {new_user_id}")
    else:
        print(f"No scores found for user_id {old_user_id}")

except Exception as e:
    print(f"An error occurred: {e}")
    session.rollback()

finally:
    # Close the session
    session.close()
"""
list_of_users = session.query(User).all()
import requests

webhook_url = "https://chat.googleapis.com/v1/spaces/AAAAzVxtSfs/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=apnWZYEA4lf78HHwfFBZYTl0aDCdnxJtKHpeHiYs4C4"  # Replace with your webhook URL
message = {"text": "Hello, " + list_of_users[2].username}

response = requests.post(webhook_url, json=message)

if response.status_code == 200:
    print("Message sent successfully!")
else:
    print(f"Failed to send message: {response.status_code}, {response.text}")
