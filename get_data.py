from pywinauto import Application, Desktop, timings
from time import sleep

def get_windows():
    windows = Desktop(backend='uia').windows()
    return windows

def get_ids(wrapper):
    return wrapper.handle, wrapper.process_id()

def get_wrapper(handle, pid):
    app = Application(backend='uia')
    spec = app.connect(process=pid)
    wrapper = spec.window(handle=handle)
    return wrapper

def clean_song(wrapper):
    song_name = wrapper.window_text()
    song_name = song_name.replace(' - YouTube - Brave', '')
    song_name = song_name.replace(' - YouTube: reproducción de audio - Brave', '')
    return song_name
    
def get_data(wrapper):
    try: 
        wrapper_child = wrapper.child_window(title="Barra de direcciones y de búsqueda ", control_type="Edit")
        url = wrapper_child.get_value()
        song_id = url.split('=')[1]
        song_id = song_id.split('&')[0]
        return (clean_song(wrapper), song_id)
    except:
        return None
