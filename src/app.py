"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}

# ...existing code...
# Add additional activities
activities.update({
    "basketball": {
        "description": "5-a-side basketball games for all skill levels.",
        "participants": [],
        "max_participants": 10,
        "category": "sports"
    },
    "swimming": {
        "description": "Lap swimming and technique practice at the campus pool.",
        "participants": [],
        "max_participants": 12,
        "category": "sports"
    },
    "painting_workshop": {
        "description": "Beginner-friendly acrylic painting sessions.",
        "participants": [],
        "max_participants": 8,
        "category": "artistic"
    },
    "sculpture_class": {
        "description": "Hands-on clay sculpture projects.",
        "participants": [],
        "max_participants": 8,
        "category": "artistic"
    },
    "chess_club": {
        "description": "Weekly chess practice and friendly tournaments.",
        "participants": [],
        "max_participants": 16,
        "category": "intellectual"
    },
    "debate_club": {
        "description": "Meetups to practice public speaking and structured debates.",
        "participants": [],
        "max_participants": 20,
        "category": "intellectual"
    }
})
# ...existing code...

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Prevent duplicate signups
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
    
    # Prevent over-capacity
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is at full capacity") 

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
