from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
from kivy.clock import Clock
from database import DatabaseManager
from utils import get_current_date_str, get_current_week_start_end, get_previous_week_start_end, format_weight
from datetime import datetime, timedelta

class WeightEntryRow(BoxLayout):
    date_text = StringProperty()
    weight_text = StringProperty()

class WeeklyAverageRow(BoxLayout):
    week_start_date_text = StringProperty()
    average_weight_text = StringProperty()
    entry_count_text = StringProperty()

class WeightTrackerApp(App):
    db_manager = ObjectProperty(None)
    current_week_entries_data = ListProperty([])
    weekly_averages_data = ListProperty([])
    current_week_average_text = StringProperty("Current Week Average: --")

    def build(self):
        self.db_manager = DatabaseManager(db_name="/home/ubuntu/kivy_weight_tracker/data/weight_tracker.db")
        self.load_data()
        Clock.schedule_interval(self.check_and_process_weekly_average, 60 * 60 * 24) # Check once a day
        return WeightTrackerLayout()

    def on_start(self):
        # Ensure data is loaded when app starts
        self.load_data()

    def load_data(self):
        self.load_current_week_data()
        self.load_weekly_averages()

    def load_current_week_data(self):
        start_date, end_date = get_current_week_start_end()
        entries = self.db_manager.get_weight_entries_for_week(start_date, end_date)
        self.current_week_entries_data = [{
            'date_text': date,
            'weight_text': f"{format_weight(weight)} kg"
        } for date, weight in entries]

        avg_weight = self.db_manager.get_average_weight_for_week(start_date, end_date)
        entry_count = self.db_manager.get_entry_count_for_week(start_date, end_date)

        if entry_count > 0:
            self.current_week_average_text = f"Current Week Average: {format_weight(avg_weight)} kg ({entry_count} entries)"
        else:
            self.current_week_average_text = "Current Week Average: --"

    def load_weekly_averages(self):
        averages = self.db_manager.get_all_weekly_averages()
        self.weekly_averages_data = [{
            'week_start_date_text': f"Week of {week_start_date}",
            'average_weight_text': f"{format_weight(average_weight)} kg",
            'entry_count_text': f"({entry_count} entries)"
        } for week_start_date, average_weight, entry_count in averages]

    def add_weight(self, weight_input_text):
        try:
            weight = float(weight_input_text)
            if weight <= 0:
                self.root.ids.status_label.text = "Please enter a valid weight."
                return

            current_date = get_current_date_str()
            if self.db_manager.add_weight_entry(current_date, weight):
                self.root.ids.weight_input.text = ""
                self.root.ids.status_label.text = "Weight added successfully!"
                self.load_current_week_data()
            else:
                self.root.ids.status_label.text = "Failed to add weight."
        except ValueError:
            self.root.ids.status_label.text = "Invalid weight. Please enter a number."

    def check_and_process_weekly_average(self, dt):
        # This function will be called periodically (e.g., daily)
        # It checks if a new week has started and processes the previous week's average
        
        # Get the start date of the current week
        current_week_start_str, _ = get_current_week_start_end()
        current_week_start_date = datetime.strptime(current_week_start_str, '%Y-%m-%d').date()

        # Get the start date of the last processed week from the database
        # For simplicity, let's assume we store the last processed week's start date in a separate table or file
        # For now, we'll just process the previous week if it hasn't been processed.
        
        # Get previous week's start and end dates
        prev_week_start_str, prev_week_end_str = get_previous_week_start_end()
        
        # Check if this previous week has already been processed
        # This is a simplified check. In a real app, you'd have a flag or check the weekly_averages table
        # to see if an entry for prev_week_start_str already exists.
        processed_averages = self.db_manager.get_all_weekly_averages()
        already_processed = False
        for ws_date, _, _ in processed_averages:
            if ws_date == prev_week_start_str:
                already_processed = True
                break

        if not already_processed:
            # Calculate average for the previous week
            avg_weight = self.db_manager.get_average_weight_for_week(prev_week_start_str, prev_week_end_str)
            entry_count = self.db_manager.get_entry_count_for_week(prev_week_start_str, prev_week_end_str)

            if entry_count > 0:
                self.db_manager.add_weekly_average(prev_week_start_str, avg_weight, entry_count)
                self.load_weekly_averages()
                print(f"Processed weekly average for {prev_week_start_str}")
            else:
                print(f"No entries for week {prev_week_start_str}, skipping average calculation.")

class WeightTrackerLayout(BoxLayout):
    pass

if __name__ == '__main__':
    WeightTrackerApp().run()


