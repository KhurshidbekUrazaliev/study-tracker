from datetime import datetime, timedelta
from tracker.storage import load_data, save_data

# Define our habits
HABITS = [
    "Programming",
    "Language learning",
    "Qur'an reading",
    "Reading books",
    "Workout",
    "Capital"
]

def log_completion(habit_name, date=None):
    """
    Log a habit as completed for a given date.
    
    Args:
        habit_name: Name of the habit
        date: Date string in YYYY-MM-DD format (defaults to today)
    """
    if habit_name not in HABITS:
        raise ValueError(f"Unknown habit: {habit_name}")
    
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    data = load_data()
    
    # Initialize habit if it doesn't exist
    if habit_name not in data:
        data[habit_name] = []
    
    # Add date if not already logged
    if date not in data[habit_name]:
        data[habit_name].append(date)
        data[habit_name].sort()  # Keep dates sorted
    
    save_data(data)

def calculate_streak(habit_name):
    """
    Calculate current streak for a habit.
    
    Returns:
        int: Number of consecutive days (including today if completed)
    """
    data = load_data()
    
    if habit_name not in data or not data[habit_name]:
        return 0
    
    dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in data[habit_name]]
    dates.sort(reverse=True)  # Most recent first
    
    today = datetime.now().date()
    
    # Check if today or yesterday was completed
    # (we allow yesterday as "current" to avoid breaking streaks)
    if dates[0] != today and dates[0] != today - timedelta(days=1):
        return 0
    
    # Count consecutive days
    streak = 1
    expected_date = dates[0] - timedelta(days=1)
    
    for date in dates[1:]:
        if date == expected_date:
            streak += 1
            expected_date -= timedelta(days=1)
        else:
            break
    
    return streak

def get_all_streaks():
    """Get current streaks for all habits."""
    return {habit: calculate_streak(habit) for habit in HABITS}

def is_completed_today(habit_name):
    """Check if a habit was completed today."""
    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    
    return habit_name in data and today in data[habit_name]