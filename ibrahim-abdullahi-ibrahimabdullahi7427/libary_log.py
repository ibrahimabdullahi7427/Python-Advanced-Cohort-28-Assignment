import os
import time
from datetime import datetime, timedelta

# Custom exception for duplicate visitor
class DuplicateVisitorError(Exception):
    pass

# Custom exception for lock timing
class VisitorLockError(Exception):
    pass

FILE_NAME = "visitors.txt"
LOCK_FILE = "lock.txt"

def get_last_visitor():
    """Return the last visitor's name from visitors.txt if it exists."""
    if not os.path.exists(FILE_NAME):
        return None
    with open(FILE_NAME, "r") as file:
        lines = file.readlines()
        if not lines:
            return None
        last_line = lines[-1].strip()
        if last_line:
            return last_line.split(" - ")[0]  # name before timestamp
    return None

def get_lock_status():
    """Check if lock is active, return True if still within 5 minutes."""
    if os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, "r") as file:
            timestamp_str = file.read().strip()
            if timestamp_str:
                lock_time = datetime.fromisoformat(timestamp_str)
                if datetime.now() < lock_time + timedelta(minutes=5):
                    return True
    return False

def set_lock():
    """Set lock with current time."""
    with open(LOCK_FILE, "w") as file:
        file.write(datetime.now().isoformat())

def add_visitor():
    try:
        # Check lock
        if get_lock_status():
            raise VisitorLockError("Another visitor is still inside. Please wait 5 minutes.")

        visitor_name = input("Enter visitor's name: ").strip()
        last_visitor = get_last_visitor()

        if visitor_name == last_visitor:
            raise DuplicateVisitorError(f"Duplicate entry: {visitor_name} is the same as last visitor.")

        # Add visitor with timestamp
        with open(FILE_NAME, "a") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{visitor_name} - {timestamp}\n")

        # Set lock
        set_lock()
        print(f"Welcome {visitor_name}! Entry recorded at {timestamp}.")

    except DuplicateVisitorError as e:
        print(f"Error: {e}")
    except VisitorLockError as e:
        print(f"Access Denied: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run program
if __name__ == "__main__":
    add_visitor()
