#!/usr/bin/env python3
"""
Smart Study & Discipline Tracker
A CLI tool for tracking daily habits and building streaks.
"""

import sys
from datetime import datetime
from tracker.habits import (
    HABITS,
    log_completion,
    get_all_streaks,
    is_completed_today
)

def print_banner():
    """Print a simple banner."""
    print("\n" + "="*50)
    print("  📚 STUDY & DISCIPLINE TRACKER")
    print("="*50 + "\n")

def cmd_log(habit_name):
    """Log a habit completion."""
    if habit_name not in HABITS:
        print(f"❌ Unknown habit: '{habit_name}'")
        print(f"\nAvailable habits:")
        for h in HABITS:
            print(f"  - {h}")
        return
    
    try:
        log_completion(habit_name)
        streak = get_all_streaks()[habit_name]
        print(f"✅ Logged: {habit_name}")
        print(f"🔥 Current streak: {streak} days")
    except Exception as e:
        print(f"❌ Error: {e}")

def cmd_status():
    """Show status of all habits."""
    print_banner()
    
    streaks = get_all_streaks()
    today = datetime.now().strftime("%A, %B %d, %Y")
    print(f"📅 {today}\n")
    
    print("HABIT STATUS:")
    print("-" * 50)
    
    for habit in HABITS:
        streak = streaks[habit]
        completed = is_completed_today(habit)
        
        status_icon = "✅" if completed else "⬜"
        fire_emoji = "🔥" if streak > 0 else "  "
        
        print(f"{status_icon} {habit:25} {fire_emoji} {streak:2} days")
    
    print("-" * 50)
    total_completed = sum(1 for h in HABITS if is_completed_today(h))
    print(f"\n📊 Completed today: {total_completed}/{len(HABITS)}")
    print()

def cmd_summary():
    """Show weekly summary."""
    from tracker.stats import get_weekly_summary, get_total_completions_this_week, get_best_habit
    
    print_banner()
    print("📊 WEEKLY SUMMARY (Last 7 Days)\n")
    
    summary = get_weekly_summary()
    
    print("COMPLETION RATES:")
    print("-" * 50)
    
    for habit in HABITS:
        stats = summary[habit]
        count = stats["completed_days"]
        rate = stats["completion_rate"]
        
        # Visual bar
        bar_length = int(rate / 10)
        bar = "█" * bar_length + "░" * (10 - bar_length)
        
        print(f"{habit:25} {bar} {count}/7 ({rate:.0f}%)")
    
    print("-" * 50)
    
    total = get_total_completions_this_week()
    possible = len(HABITS) * 7
    overall_rate = (total / possible) * 100
    
    print(f"\n📈 Total completions: {total}/{possible} ({overall_rate:.0f}%)")
    
    best = get_best_habit()
    if best:
        habit_name, count = best
        print(f"🏆 Best habit: {habit_name} ({count} days)")
    
    print()

def cmd_help():
    """Show help message."""
    print_banner()
    print("USAGE:")
    print("  python main.py log <habit>    Log a habit completion")
    print("  python main.py status         Show all habits and streaks")
    print("  python main.py summary        Show weekly summary")
    print("  python main.py help           Show this help message")
    print("\nAVAILABLE HABITS:")
    for habit in HABITS:
        print(f"  - {habit}")
    print()

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        cmd_status()
        return
    
    command = sys.argv[1].lower()
    
    if command == "log":
        if len(sys.argv) < 3:
            print("❌ Usage: python main.py log <habit>")
            return
        habit_name = " ".join(sys.argv[2:])
        cmd_log(habit_name)
    
    elif command == "status":
        cmd_status()
    
    elif command == "summary":
        cmd_summary()
    
    elif command == "help":
        cmd_help()
    
    else:
        print(f"❌ Unknown command: '{command}'")
        print("Run 'python main.py help' for usage.")

if __name__ == "__main__":
    main()