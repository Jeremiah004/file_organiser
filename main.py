import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def organize_files(src_folder):
    file_types = {
        'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
        'documents': ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx'],
        'videos': ['.mp4', '.mkv', '.flv', '.avi', '.mov'],
        'music': ['.mp3', '.wav', '.aac'],
        'archives': ['.zip', '.rar', '.tar', '.gz'],
        'scripts': ['.py', '.js', '.html', '.css'],
        'others': []
    }
    
    for filename in os.listdir(src_folder):
        src_path = os.path.join(src_folder, filename)
        
        if os.path.isfile(src_path):
            file_ext = os.path.splitext(filename)[1].lower()
            moved = False
            
            for folder, extensions in file_types.items():
                if file_ext in extensions:
                    dest_folder = os.path.join(src_folder, folder)
                    if not os.path.exists(dest_folder):
                        os.makedirs(dest_folder)
                    shutil.move(src_path, os.path.join(dest_folder, filename))
                    moved = True
                    break
            
            if not moved:
                dest_folder = os.path.join(src_folder, 'others')
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                shutil.move(src_path, os.path.join(dest_folder, filename))
                
class FileHandler(FileSystemEventHandler):
    def __init__(self, src_folder):
        self.src_folder = src_folder

    def on_modified(self, event):
        organize_files(self.src_folder)

if __name__ == "__main__":
    src_folder = '/path/to/your/folder'  # Update with your folder path
    event_handler = FileHandler(src_folder)
    observer = Observer()
    observer.schedule(event_handler, path=src_folder, recursive=False)
    observer.start()

    try:
        while True:
            pass  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
