# Experimental Now Playing App for YouTube Songs
A PyQt5 app that displays the song you are playing on youtube. Useful for OBS Now Playing in YouTube instead of Spotify.

## How to use it
Note that this is an experimental app, its quite buggy and not meant for normal use.
There won't be any releases until I come back to this project, so for now you can:

1. Run `listener.py`. It will print the windows handle & process id of your opened windows in a tuple.
2. Copy your 2 windows handle and PID and paste them in `main.py` inside the class Worker (you should paste them into this 2 variables: handle and pid).
3. Run `main.py`
