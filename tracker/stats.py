from datetime import datetime, timedelta
from tracker.storage import load_data
from tracker.habits import HABITS

def get_weekly_summary():
    """
    Generate a summary of the last 7 days.
    
    Returns:
        dict: Weekly statistics for each habit
    """
    data = load_data()
    today = datetime.now().date()
    week_ago = today - timedelta(days=6)  # Last 7 days including today
    
    summary = {}
    
    for habit in HABITS:
        completed_dates = []
        
        if habit in data:
            # Convert stored dates to date objects
            all_dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in data[habit]]
            # Filter to last 7 days
            completed_dates = [d for d in all_dates if week_ago <= d <= today]
        
        completion_count = len(completed_dates)
        completion_rate = (completion_count / 7) * 100
        
        summary[habit] = {
            "completed_days": completion_count,
            "completion_rate": completion_rate,
            "dates": completed_dates
        }
    
    return summary

def get_total_completions_this_week():
    """Get total number of habit completions this week."""
    summary = get_weekly_summary()
    return sum(stats["completed_days"] for stats in summary.values())

def get_best_habit():
    """Find the habit with the highest completion rate this week."""
    summary = get_weekly_summary()
    
    if not summary:
        return None
    
    best = max(summary.items(), key=lambda x: x[1]["completed_days"])
    
    if best[1]["completed_days"] == 0:
        return None
    
    return best[0], best[1]["completed_days"]

def get_completion_calendar(habit_name, days=7):
    """
    Get a visual calendar of completions for a habit.
    
    Returns:
        list: List of (date, completed) tuples for the last N days
    """
    data = load_data()
    today = datetime.now().date()
    
    calendar = []
    
    for i in range(days - 1, -1, -1):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        
        completed = habit_name in data and date_str in data[habit_name]
        calendar.append((date, completed))
    
    return calendar