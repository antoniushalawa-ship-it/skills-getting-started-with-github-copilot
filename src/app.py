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

# In-memory activity database (extra entries will be merged at startup)
extra_activities = {
    # Sports (2)
    "Soccer Club": {
        "description": "Outdoor team sport focusing on skills, tactics, and matches",
        "schedule": "Tuesdays & Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Indoor team sport, drills and friendly competitions",
        "schedule": "Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu"]
    },

    # Artistic (2)
    "Drama Club": {
        "description": "Acting, stagecraft, and school play productions",
        "schedule": "Mondays & Wednesdays, 5:00 PM - 6:30 PM",
        "max_participants": 25,
        "participants": ["isabella@mergington.edu"]
    },
    "Art Club": {
        "description": "Drawing, painting, and portfolio development",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["noah@mergington.edu"]
    },

    # Intellectual (2)
    "Science Club": {
        "description": "Hands-on experiments, research projects, and science fair prep",
        "schedule": "Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 18,
        "participants": ["mia@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Problem solving, training, and competition preparation",
        "schedule": "Saturdays, 10:00 AM - 12:00 PM",
        "max_participants": 10,
        "participants": ["lucas@mergington.edu"]
    }
}

@app.on_event("startup")
def populate_extra_activities():
    # Merge extra_activities into the main activities store without overwriting existing keys
    for name, info in extra_activities.items():
        if name not in activities:
            activities[name] = info
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

    # Add student

    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
