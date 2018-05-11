# WebApp music controller #

cmus
----
**cmus** is a fast and light music player for Unix-like operating systems. It's intended to be used mostly by the console, but it also opens a TCP port in the system which creates a new way to interact with it for the use.

Flask
-----
Taking advantage of this fact,

Setting up
----------
In order to create the server, we need to be sure we have Flask installed in our system. It's suggested to use a virtual environment for that:
```console
user@system:~/webapp-musiccontroller-raspberry$ python3 -m venv venv
user@system:~/webapp-musiccontroller-raspberry$ source venv/bin/activate
(venv) user@system:~/webapp-musiccontroller-raspberry$ pip install Flask

```