import time

class Command:
    def execute(self):
        raise NotImplementedError()

class StartChecksCommand(Command):
    def __init__(self, rocket, altitude_threshold, fuel_decrement, altitude_increase, speed_increase):
        self.rocket = rocket
        self.altitude_threshold = altitude_threshold
        self.fuel_decrement = fuel_decrement
        self.altitude_increase_per_second = altitude_increase
        self.speed_increase_per_iteration = speed_increase

    def execute(self):
        self.rocket.start_checks(self.altitude_threshold, self.fuel_decrement, self.altitude_increase_per_second, self.speed_increase_per_iteration)

class LaunchCommand(Command):
    def __init__(self, rocket):
        self.rocket = rocket

    def execute(self):
        self.rocket.launch()

class FastForwardCommand(Command):
    def __init__(self, rocket, seconds):
        self.rocket = rocket
        self.seconds = seconds

    def execute(self):
        self.rocket.fast_forward(self.seconds)
        self.rocket.update_status() 

class Observable:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update()

class LoggingObserver:
    def __init__(self):
        pass

    def update(self):
        pass

    def log(self, message):
        print(message)

class Rocket(Observable):
    def __init__(self):
        super().__init__()
        self.stage = "Pre-Launch"
        self.fuel = 100
        self.altitude = 0
        self.speed = 0
        self.altitude_threshold = None
        self.fuel_decrement = None
        self.altitude_increase_per_second = None
        self.speed_increase_per_iteration = None
    def reset(self):
        self.fuel = 100
        self.altitude = 0
        self.speed = 0
    def start_checks(self, altitude_threshold, fuel_decrement, altitude_increase, speed_increase):
        self.altitude_threshold = altitude_threshold
        self.fuel_decrement = fuel_decrement
        self.altitude_increase_per_second = altitude_increase
        self.speed_increase_per_iteration = speed_increase
        print("Running system checks...")
        time.sleep(2)
        print("All systems are 'Go' for launch.")
        self.notify_observers()

    def launch(self):
        if self.stage == "Pre-Launch":
            print("Launching...")
            self.stage = "Stage 1"
            self.update_status_continuously()

    def update_status_continuously(self):
        while self.altitude < self.altitude_threshold and self.fuel > 0:
            self.update_status1()
            time.sleep(1)
            self.notify_observers()
            
        if self.altitude >= self.altitude_threshold:
            print("Stage 1 complete. Separating stage. Entering Stage 2.")
            print("Orbit achieved! Mission Successful.")
            self.stage = "Orbit"
            self.notify_observers()
        else:
            print("Mission Failed due to insufficient fuel.")
            self.stage = "Failed"
            self.notify_observers()

    def fast_forward(self, seconds):
        self.reset()
        while seconds > 0 and self.altitude < self.altitude_threshold and self.fuel > 0:
            self.altitude += self.altitude_increase_per_second
            self.speed += self.speed_increase_per_iteration
            self.fuel -= self.fuel_decrement
            seconds -= 1

    def update_status1(self):
        self.altitude += self.altitude_increase_per_second
        self.speed += self.speed_increase_per_iteration
        self.fuel -= self.fuel_decrement
        print(f"Stage: {self.stage}, Fuel: {self.fuel}%, Altitude: {self.altitude} km, Speed: {self.speed} km/h")
        
    def update_status(self):
        print(f"Stage: {self.stage}, Fuel: {self.fuel}%, Altitude: {self.altitude} km, Speed: {self.speed} km/h")
        self.altitude += self.altitude_increase_per_second
        self.speed += self.speed_increase_per_iteration
        self.fuel -= self.fuel_decrement

def user_interface(rocket):
    logging_observer = LoggingObserver()
    rocket.add_observer(logging_observer)
    while True:
        user_input = input("Enter a command: ")
        command = parse_input(user_input, rocket)
        if command:
            command.execute()

def parse_input(user_input, rocket):
    if user_input == "start_checks":
        altitude_threshold = int(input("Enter altitude threshold (in km): "))
        altitude_increase = int(input("Enter altitude increase per second in simulation: "))
        speed_increase = int(input("Enter speed increase per iteration: "))
        fuel_decrement = int(input("Enter fuel decrement value (%): "))
        return StartChecksCommand(rocket, altitude_threshold, fuel_decrement, altitude_increase, speed_increase)
    elif user_input == "launch":
        return LaunchCommand(rocket)
    elif user_input.startswith("fast_forward"):
        try:
            _, time_to_advance = user_input.split()
            time_to_advance = int(time_to_advance)
            return FastForwardCommand(rocket, time_to_advance)
        except ValueError:
            print("Invalid input for fast_forward. Please enter 'fast_forward X', where X is an integer.")
    else:
        print("Invalid command. Available commands: start_checks, launch, fast_forward X")

if __name__ == "__main__":
    rocket = Rocket()
    user_interface(rocket)