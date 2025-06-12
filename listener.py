from get_data import *


windows = get_windows()
for i in range(len(windows)):
    print(i, windows[i].window_text())

print(get_ids(windows[6]))

handle, pid = 394860, 4652
wrapper = get_wrapper(handle, pid)
run = True

def main_listener():
    prev_song = clean_song(wrapper)        
    data = get_data(wrapper)
    while clean_song(wrapper) == prev_song:
        sleep(3)
    