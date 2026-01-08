from scenes.morning import MorningRoutine
from scenes.evening import EveningRoutine

class RoutineController:
    def __init__(self, bot):
        self.bot = bot
        self.current_routine = None

    def stop_current(self):
        if self.current_routine and hasattr(self.current_routine, "stop"):
            self.current_routine.stop()
        self.current_routine = None

    def start_morning(self):
        self.stop_current()
        self.current_routine = MorningRoutine(self.bot)
        self.current_routine.run()

    def start_evening(self):
        self.stop_current()
        self.current_routine = EveningRoutine(self.bot)
        result = self.current_routine.run()

        if result == "GO_TO_SLEEP":
            print("Going to sleep...")
            return True
        
        if result == "EXCEPTION_DAY":
            print("Going to sleep...")
            return False
