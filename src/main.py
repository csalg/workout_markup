#! python3
from io import *


def main():
    # Every day we check to see if a file has been modified in the past 24h
    previous_dt = load_previous_dt()
    new_files = find_new_workout_files(previous_dt)
    # If we find such a file then we attempt to parse it and persist the session.
    if new_files:
        for filename in new_files:
            try:
                session = session_load(filename)
                if session:
                    persist_session(session)
                    delete_file(filename)
            except:
                pass
    
    # On Sundays we copy a new batch of workouts for the following week.
    if is_sunday():
        copy_workout_templates_to_interaction_folder()
    
    update_nextcloud_database()
    dump_current_dt()

if __name__ == '__main__':
    main()