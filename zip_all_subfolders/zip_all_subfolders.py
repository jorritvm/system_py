import os
import zipfile

def create_zip_for_subfolders(directory):
    # Change to the target directory
    os.chdir(directory)
    
    # List all subdirectories in the current directory
    subfolders = [f.name for f in os.scandir(directory) if f.is_dir()]

    for subfolder in subfolders:
        zip_filename = f"{subfolder}.zip"
        print(f"working on {zip_filename}")
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walking through the subfolder
            for root, _, files in os.walk(subfolder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=subfolder)
                    zipf.write(file_path, arcname)

    print("Zipping completed for all subfolders.")

if __name__ == "__main__":
    print(os.getcwd())
    current_directory = os.getcwd()
    create_zip_for_subfolders(current_directory)