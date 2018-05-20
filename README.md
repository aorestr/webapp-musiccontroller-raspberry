# WebApp music controller #

The project you can find down below is made mostly for self-learning, so don't expect anything great (maybe not even good).

It has been made as a small college project whose subject has nothing to do with web applications.

The program starts a music player and a server in the system where you execute the code. You can connect to the domain with any device within the same network as the server system.

Dependencies
-----------

### cmus ###
**cmus** is a fast and light music player for Unix-like operating systems. It's intended to be used mostly by the console, but it also opens a TCP port in the system which creates a new way to interact with it for the use.

### Flask ###
**Flask** is a Python framework oriented to create and handle a server. It's supposed to be simple and easily usable.

### PyCmus ###
Small library for Python with methods for connecting to a **cmus** by sockets. Its [repo](https://github.com/mtreinish/pycmus).

### TinyTag ###
Extracts information from an audio file and stores it in an object whose attributes are the file's ones. [Repository](https://github.com/mtreinish/pycmus).


Usage
-----
### Setting up ###
In order to create the server, you need to be sure you have Flask installed in our system. It's suggested to use a virtual environment for that:
```console
user@system:~/webapp-musiccontroller-raspberry$ python3 -m venv venv
user@system:~/webapp-musiccontroller-raspberry$ source venv/bin/activate
(venv) user@system:~/webapp-musiccontroller-raspberry$ pip install Flask
```
Of course, you will also need **cmus** in order to play the music. If we use a Debian-based distro, we just need to execute:
```console
user@system:~$ sudo apt install cmus 
```

### Open **cmus** and the server ###
Once it's everything settle down, run *run_webapp.py* in the terminal. You can use the flags:
* **-p**: choose the number of the port in which the webapp will be running. 5000 by default.
* **-mf**: you can pass the path of the folder where your music will be stored. It's in *root/music* by default.

After execution, the programm will try to open a **cmus** instance in case it's not opened, analizes the music files and then loads the webpage.
Then, type at your browser: **[server_local_IP][webapp_port]**, where the first term is the IP your machine has locally (ex, 192.168.1.36) and the port is the one you have chosen previously. Et voilà, you can control your player (in a very basic way) through another device in the same network.

Limitations
-----------
As it's already said, the application is extremely basic. I didn't try to create anything new or better but to learn the foundamentals on this kind of stuff. The application is slow, is not threats-proof at all, breaks it easily, you can read music from only a directory, the player has too few funtionalities and so on.

However, I have learnt how to open a server, how to load a domain, how to make it dinamic, how to interact with it (I didn't know JavaScript, CSS or HTML at all before this!), how to exchange data between the backend and the frontend... I think I have reached my goal.