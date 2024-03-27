import os
import datetime


def modify_cm_time_safe(folder_path, days=0, hours=0, minutes=0):
    # get confirmation first
    confirmation = input(
        f"Are you sure you want to modify the contents of this folder {folder_path} and its subfolders (yes/no)?"
    )
    if confirmation.lower() != "yes":
        print("Operation cancelled.")
        return
    else:
        modify_cm_time(folder_path, days, hours, minutes)


def modify_cm_time(folder_path, days=0, hours=0, minutes=0):
    # delta to add to original cm times
    time_delta = datetime.timedelta(days=days, hours=hours, minutes=minutes)

    # iterate over all files and adapt the cm times
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            created_time = os.path.getctime(file_path)
            modified_time = os.path.getmtime(file_path)

            new_created_time = created_time + time_delta.total_seconds()
            new_modified_time = modified_time + time_delta.total_seconds()

            # update the times
            os.utime(file_path, (new_created_time, new_modified_time))

            print(f"Modified times for {file_path}")


if __name__ == "__main__":
    folder_path = r"PASTE HERE"
    modify_cm_time_safe(folder_path, 1, 3)
