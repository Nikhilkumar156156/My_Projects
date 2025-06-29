import os

# Set your folder path here
folder_path = r"path"  # Replace 'path' with your actual folder path
# Set the starting number
start_number = 130

# Get list of files
files = os.listdir(folder_path)
files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]

# Sort files by name (you can sort by date if needed)
files.sort()

# Rename files with zero-padded numbers
for i, filename in enumerate(files, start=start_number):
    name, ext = os.path.splitext(filename)
    new_name = f"{i:04d}{ext}"  # Format: 0000, 0001, etc.

    old_path = os.path.join(folder_path, filename)
    new_path = os.path.join(folder_path, new_name)

    try:
        os.rename(old_path, new_path)
        print(f"Renamed '{filename}' -> '{new_name}'")
    except Exception as e:
        print(f"Error renaming '{filename}': {e}")
