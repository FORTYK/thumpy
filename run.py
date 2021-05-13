import time, glob, os
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

EXECUTION_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(EXECUTION_PATH, 'img')
OUTPUT_DIR = os.path.join(EXECUTION_PATH, 'thumbnails')

PREFIX = 't_'
SIZE = 68,68

class Watcher:

  def __init__(self):
    self.observer = Observer()

  def run(self):
    event_handler = Handler()
    self.observer.schedule(event_handler, INPUT_DIR, recursive=True)
    self.observer.start()
    try:
      while True:
        time.sleep(5)
    except:
      self.observer.stop()
      print("Error")

    self.observer.join()

class Handler(FileSystemEventHandler):

  @staticmethod
  def on_any_event(event):
    file_path = os.path.abspath(event.src_path)
    file_name = os.path.basename(file_path)

    print(event.event_type, PREFIX + file_name, SIZE, ' FROM: ', file_path)

    if event.is_directory:
      return None

    elif event.event_type == 'deleted':
      Thumbnailer().remove(file_path)

    elif event.event_type == 'moved':
      Thumbnailer().remove(file_path)

    elif event.event_type == 'created':
      Thumbnailer().create(file_path)

    elif event.event_type == 'modified':
      Thumbnailer().remove(file_path)
      Thumbnailer().create(file_path)

class Thumbnailer():
  @staticmethod
  def exists(file_path):
    return os.path.exists(file_path)

  @staticmethod
  def remove(file_path):
    file_name = os.path.basename(file_path)

    thumbnail_path = os.path.join(OUTPUT_DIR, PREFIX + str(SIZE[0]) + "_" + str(SIZE[1]) + "_" + file_name);
    isExists = Thumbnailer.exists(thumbnail_path)

    if(isExists):
      os.remove(thumbnail_path)
    
    
  @staticmethod
  def create(file_path):
    file_name = os.path.basename(file_path)
    thumbnail_path = os.path.join(OUTPUT_DIR, PREFIX + str(SIZE[0]) + "_" + str(SIZE[1]) + "_" + file_name);

    try:
      # Scaling the img to fit size
      image = Image.open(file_path)
      image.thumbnail(SIZE, Image.ANTIALIAS)

      # Adding background to scaled img
      background = Image.new('RGBA', SIZE, (255, 255, 255, 0))
      background.paste(
          image, (int((SIZE[0] - image.size[0]) / 2), int((SIZE[1] - image.size[1]) / 2))
      )
      background.save(thumbnail_path, "png", optimize=True,quality=95)
    except IOError:
      print('Could not create thumbnail: ',thumbnail_path)
    

if __name__ == '__main__':
  w = Watcher()
  w.run()        