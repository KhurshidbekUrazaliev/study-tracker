import unittest
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from tracker.habits import log_completion, calculate_streak, get_all_streaks, is_completed_today, HABITS
from tracker.stats import get_weekly_summary, get_total_completions_this_week, get_best_habit
from tracker import storage

class TestHabitTracking(unittest.TestCase):
    """Test suite for habit tracking functionality."""
    
    def setUp(self):
        """Set up test environment before each test."""
        # Create a temporary test data file
        self.test_data_file = Path("tests/test_progress.json")
        
        # Backup original DATA_FILE path
        self.original_data_file = storage.DATA_FILE
        
        # Override DATA_FILE for testing
        storage.DATA_FILE = self.test_data_file
        
        # Clear test data
        if self.test_data_file.exists():
            self.test_data_file.unlink()
    
    def tearDown(self):
        """Clean up after each test."""
        # Remove test file
        if self.test_data_file.exists():
            self.test_data_file.unlink()
        
        # Restore original DATA_FILE
        storage.DATA_FILE = self.original_data_file
    
    def test_log_completion_creates_new_habit(self):
        """Test logging a habit for the first time."""
        habit = HABITS[0]
        today = datetime.now().strftime("%Y-%m-%d")
        
        log_completion(habit)
        data = storage.load_data()
        
        self.assertIn(habit, data)
        self.assertIn(today, data[habit])
    
    def test_log_completion_no_duplicates(self):
        """Test that logging the same habit twice on the same day doesn't create duplicates."""
        habit = HABITS[0]
        
        log_completion(habit)
        log_completion(habit)
        
        data = storage.load_data()
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Should only have one entry for today
        self.assertEqual(data[habit].count(today), 1)
    
    def test_log_completion_invalid_habit(self):
        """Test that logging an invalid habit raises an error."""
        with self.assertRaises(ValueError):
            log_completion("Invalid Habit")
    
    def test_calculate_streak_no_data(self):
        """Test streak calculation with no data."""
        habit = HABITS[0]
        streak = calculate_streak(habit)
        
        self.assertEqual(streak, 0)
    
    def test_calculate_streak_single_day(self):
        """Test streak calculation with one day logged."""
        habit = HABITS[0]
        today = datetime.now().strftime("%Y-%m-%d")
        
        storage.save_data({habit: [today]})
        streak = calculate_streak(habit)
        
        self.assertEqual(streak, 1)
    
    def test_calculate_streak_consecutive_days(self):
        """Test streak calculation with consecutive days."""
        habit = HABITS[0]
        today = datetime.now().date()
        
        dates = [
            (today - timedelta(days=2)).strftime("%Y-%m-%d"),
            (today - timedelta(days=1)).strftime("%Y-%m-%d"),
            today.strftime("%Y-%m-%d")
        ]
        
        storage.save_data({habit: dates})
        streak = calculate_streak(habit)
        
        self.assertEqual(streak, 3)
    
    def test_calculate_streak_broken(self):
        """Test that a broken streak resets to 0."""
        habit = HABITS[0]
        today = datetime.now().date()
        
        # Last completion was 3 days ago (broken streak)
        old_date = (today - timedelta(days=3)).strftime("%Y-%m-%d")
        
        storage.save_data({habit: [old_date]})
        streak = calculate_streak(habit)
        
        self.assertEqual(streak, 0)
    
    def test_is_completed_today_true(self):
        """Test checking if habit was completed today."""
        habit = HABITS[0]
        log_completion(habit)
        
        self.assertTrue(is_completed_today(habit))
    
    def test_is_completed_today_false(self):
        """Test checking if habit was not completed today."""
        habit = HABITS[0]
        
        self.assertFalse(is_completed_today(habit))
    
    def test_get_all_streaks(self):
        """Test getting streaks for all habits."""
        habit1 = HABITS[0]
        habit2 = HABITS[1]
        today = datetime.now().strftime("%Y-%m-%d")
        
        storage.save_data({
            habit1: [today],
            habit2: [today]
        })
        
        streaks = get_all_streaks()
        
        self.assertEqual(streaks[habit1], 1)
        self.assertEqual(streaks[habit2], 1)
        # Other habits should have 0 streak
        self.assertEqual(streaks[HABITS[2]], 0)

class TestWeeklySummary(unittest.TestCase):
    """Test suite for weekly summary functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_data_file = Path("tests/test_progress.json")
        
        self.original_data_file = storage.DATA_FILE
        storage.DATA_FILE = self.test_data_file
        
        if self.test_data_file.exists():
            self.test_data_file.unlink()
    
    def tearDown(self):
        """Clean up after tests."""
        if self.test_data_file.exists():
            self.test_data_file.unlink()
        
        storage.DATA_FILE = self.original_data_file
    
    def test_weekly_summary_empty(self):
        """Test weekly summary with no data."""
        summary = get_weekly_summary()
        
        for habit in HABITS:
            self.assertEqual(summary[habit]["completed_days"], 0)
            self.assertEqual(summary[habit]["completion_rate"], 0)
    
    def test_weekly_summary_with_data(self):
        """Test weekly summary with some completions."""
        habit = HABITS[0]
        today = datetime.now().date()
        
        dates = [
            (today - timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(3)  # Last 3 days
        ]
        
        storage.save_data({habit: dates})
        summary = get_weekly_summary()
        
        self.assertEqual(summary[habit]["completed_days"], 3)
        self.assertAlmostEqual(summary[habit]["completion_rate"], 42.86, places=1)
    
    def test_get_total_completions(self):
        """Test total completions calculation."""
        today = datetime.now().date()
        dates = [today.strftime("%Y-%m-%d")]
        
        storage.save_data({
            HABITS[0]: dates,
            HABITS[1]: dates,
            HABITS[2]: dates
        })
        
        total = get_total_completions_this_week()
        self.assertEqual(total, 3)
    
    def test_get_best_habit(self):
        """Test finding the best performing habit."""
        today = datetime.now().date()
        
        storage.save_data({
            HABITS[0]: [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)],
            HABITS[1]: [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(2)]
        })
        
        best_habit, count = get_best_habit()
        
        self.assertEqual(best_habit, HABITS[0])
        self.assertEqual(count, 5)
    
    def test_get_best_habit_no_data(self):
        """Test best habit when no data exists."""
        result = get_best_habit()
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
    