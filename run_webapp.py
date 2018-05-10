#!/usr/bin/python3

from .webapp import MusicControllerWeb

if __name__ == '__main__': 
    flask_object = MusicControllerWeb(__name__)
    flask_object.app.run(debug=True, host='0.0.0.0')