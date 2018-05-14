# WebApp music controller #

The project you can find down below is made mostly for self-learning, so don't expect anything great (maybe not even good).

The program starts a music player and a server in the system where you execute the code. You can connect to the domain with any device within the same network as the server system.

Dependencies
-----------

### cmus ###
**cmus** is a fast and light music player for Unix-like operating systems. It's intended to be used mostly by the console, but it also opens a TCP port in the system which creates a new way to interact with it for the use.

### Flask ###
Taking advantage of this fact, 


Usage
-----
### Setting up ###
In order to create the server, we need to be sure we have Flask installed in our system. It's suggested to use a virtual environment for that:
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

Limitations
-----------
As it's already said, the application is extremely basic. I didn't try to create anything new or better but to learn the foundamentals on this kind of stuff. The application is slow, is not threats-proof at all, breaks it easily, you can read music from only a directory, the player has too few funtionalities and so on.

However, I have learnt how to open a server, how to load a domain, how to make it dinamic, how to interact with it (I didn't know JavaScript at all before this!), how to exchange data between the backend and the frontend... I think I have reached my goal.