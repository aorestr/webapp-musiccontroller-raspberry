#!/usr/bin/python3

from webserver.webapp import MusicControllerWeb
from sys import argv
from pycmus import remote, exceptions

import sys
import os
import time

if __name__ == '__main__':

    # Create a new process in which execute cmus
    try:
        import subprocess
        cmus_process = subprocess.Popen(args=["cmus"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except Exception as err:
        print('Impossible to open a new cmus instance: ', end='')
        print(err)
    finally:
        # Try to connect to cmus server
        max_time = 5
        start_time = time.time()
        while True:
            try:
                cmus = remote.PyCmus()
                break
            except exceptions.CmusNotRunning:
                if (time.time() - start_time <= max_time):
                    # If connection has been rejected but
                    # the max time hasn't passed, we try
                    # agains
                    time.sleep(1)
                    continue 
                else:
                    print('Impossible to connect to cmus. Exiting the program...')
                    try:
                        cmus_process.terminate()
                    except OSError:
                        pass
                    sys.exit(1)
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
                debug=False,
                host='0.0.0.0',
                threaded=True,
                port=port
            )
        except Exception as err:
            print('Some problem occured: ', end='')
            print(err)
            sys.exit('Exiting program...')
        # Before leaving the program, we close
        # the fork with cmus
        try:
            cmus_process.terminate()
        except OSError:
            pass