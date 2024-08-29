"""
Recursively traverse through a folder, counting files in each subfolder and its children.
Identify specific folders (named "renv", "venv", ".venv") as "ready for zipping" and replaces their count with 1 in the tree.
Identify folders with a file count higher than a specified threshold and marks them as "ready for zipping."
If some folders have to be zipped, but in their lineage a parent folder has to be zipped too, only the parent is zipped
Zips all folders marked as "ready for zipping" and removes the original from the file system.

Author: Jorrit Vander Mynsbrugge
"""

import os
import zipfile

ROOT_DIR = r"C:\Users\jorrit\drive\vub\_al merged met education\2023-2024 software engineering"  # Set the folder to search
THRESHOLD = 250  # Set the threshold for folder count
ALWAYS_ZIP = ["renv", "venv", ".venv"]  # set the folders the script must always zip
DRY_RUN = False  # set to true if you want to see the impact without changing the FS


def list_files_and_dirs(path):
    contents = os.listdir(path)
    files =  [f for f in contents if os.path.isfile(os.path.join(path, f))]
    dirs = [d for d in contents if os.path.isdir(os.path.join(path, d))]
    return files, dirs


class CountNode:
    def __init__(self, prefix, name):
        self.prefix = prefix
        self.name = name
        self.full_path = str(os.path.join(prefix, name))
        self.children = []  # list of CountNodes
        self.count = 0

    def traverse_count(self):
        files, dirs = list_files_and_dirs(self.full_path)

        # if the amount of files in this folder alone exceeds the threshold add it to the ziplist
        # and avoid further tree traversal
        if len(files) > THRESHOLD:
            self.count = 1
            print(f"this folder is too large: {self.full_path}")
            ready_for_zipping.append(self.full_path)
        elif self.name.lower() in ALWAYS_ZIP:
            self.count = 1
            ready_for_zipping.append(self.full_path)
            print(f"this folder is always zip: {self.full_path}")
        else:
            # if there are sub folders these are the children and they get calculated first
            self.children = [CountNode(self.full_path, d) for d in dirs]
            for child in self.children:
                child.traverse_count()
            # when the children are done we get the total count
            for child in self.children:
                self.count += child.count
                self.count += len(files)
            # if the THRESHOLD is exceeded we add this too the ziplist too
            if self.count > THRESHOLD:
                self.count = 1
                ready_for_zipping.append(self.full_path)
                print(f"this folder too large with its subfolders: {self.full_path}")


def remove_nested_zips(initial_list):
    # Create a copy of the list to avoid modifying it while iterating
    result = initial_list[:]
    for item in initial_list:
        for element in initial_list:
            # Ensure we are not comparing the item with itself
            if item != element and item in element:
                # Safely remove item if it's a substring of another item
                if item in result:
                    result.remove(element)
                    print(f"Removing folder because a parent also has to be zipped: {element}")
    return result


def zip_and_remove_folders(final_list):
    """
    Zips the folders marked in ready_for_zipping and removes them from the file system.
    """
    for folder in final_list:
        # Zip the folder
        zip_filename = f"{folder}.zip"
        print(f"Zipping {folder} ")
        if not DRY_RUN:
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, folder))

        # Remove the folder after zipping
        print(f"Deleting {folder}")
        if not DRY_RUN:
            for root, dirs, files in os.walk(folder, topdown=False):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                    except:
                        print(f"Could not remove {os.path.join(root, file)}, skipping...")
                for dir in dirs:
                    try:
                        os.rmdir(os.path.join(root, dir))
                    except:
                        print(f"Could not remove {os.path.join(root, dir)}, skipping...")
            try:
                os.rmdir(folder)
            except:
                print(f"Could not remove {folder}, skipping...")



if __name__ == "__main__":
    ready_for_zipping = []
    cn = CountNode(os.path.dirname(ROOT_DIR), os.path.basename(ROOT_DIR))
    cn.traverse_count()
    ready_for_zipping_top_level_only = remove_nested_zips(ready_for_zipping)
    zip_and_remove_folders(ready_for_zipping_top_level_only)




