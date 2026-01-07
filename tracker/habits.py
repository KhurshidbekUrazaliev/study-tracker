from tracker.habits import log_completion, calculate_streak, get_all_streaks

# Test logging
print("Logging Python study for today...")
log_completion("Python study")

# Test streak calculation
streak = calculate_streak("Python study")
print(f"Current streak: {streak} days")

# Test all streaks
print("\nAll streaks:")
for habit, streak in get_all_streaks().items():
    print(f"  {habit}: {streak} days")