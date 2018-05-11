#!/usr/bin/python3

from webserver.webapp import MusicControllerWeb

if __name__ == '__main__':
    from sys import argv
    
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

    flask_object = MusicControllerWeb(__name__)
    flask_object.app.run(
        debug=True,
        host='0.0.0.0',
        threaded=True,
        port=port
    )