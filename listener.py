from get_data import *


windows = get_windows()
for i in range(len(windows)):
    print(i, windows[i].window_text(), (windows[i].handle, windows[i].process_id()))

print(get_ids(windows[6]))