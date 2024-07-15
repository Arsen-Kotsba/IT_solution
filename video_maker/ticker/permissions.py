import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
video_dir = os.path.join(base_dir, "ticker/static/videos")
video_path = os.path.join(video_dir, "test_file.txt")

# Создание файла
try:
    with open(video_path, 'w') as f:
        f.write("Test content")
    print("File created successfully.")
except Exception as e:
    print(f"Error creating file: {str(e)}")

# Чтение файла
try:
    with open(video_path, 'r') as f:
        content = f.read()
    print(f"File content: {content}")
except Exception as e:
    print(f"Error reading file: {str(e)}")