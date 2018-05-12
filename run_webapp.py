#!/usr/bin/python3

from webserver.webapp import MusicControllerWeb
from sys import argv
from pycmus import remote, exceptions
from sys import exit


if __name__ == '__main__':

    try:
        cmus = remote.PyCmus()
    except exceptions.CmusNotRunning:
        # If cmus is not running we do nothing
        exit('Exiting program...')
    else:  
        # We can choose the port where we will have
        # our app running from the console
        if len(argv) == 1:
            port = None
        elif len(argv) == 2:
            try:
                port = int(argv[1])
            except ValueError as err:
                print('Invalid parameter: ', end='')
                print(err)
                print('Assigning default port')
                port = None
        else:
            print('Invalid number of parameters. Assigning default port')
            port = None
        # Open the server
        try:
            flask_object = MusicControllerWeb(__name__, cmus)
            flask_object.app.run(
                debug=True,
                host='0.0.0.0',
                threaded=True,
                port=port
            )
        except Exception as err:
            print('Some problem occurs: ', end='')
            print(err)
            exit('Exiting program...')