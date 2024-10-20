import os

# Specify the directory where the files are located
directory = "./clothes"

# List all files in the directory
files = os.listdir(directory)

# Iterate through the files and rename them based on their index
for index, filename in enumerate(files):
    # Get the file extension
    file_extension = os.path.splitext(filename)[1]
    
    # Create the new file name using the index and keep the original extension
    new_filename = f"{index+1}{file_extension}"
    
    # Get the full path for the original and new file names
    original_file = os.path.join(directory, filename)
    new_file = os.path.join(directory, new_filename)
    
    # Rename the file
    os.rename(original_file, new_file)
    
    print(f"Renamed '{filename}' to '{new_filename}'")

print("All files have been renamed.")
