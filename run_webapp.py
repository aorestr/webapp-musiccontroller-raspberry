#!./venv/bin/python3

from webserver.webapp import MusicControllerWeb
from sys import argv
from pycmus import remote, exceptions

import sys
import os
import time


def exit_cmus(cmus, cmus_process):
    """
    Closes the process with cmus that has been
    opened at the start of the program
    """
    try:
        cmus.send_cmd('quit\n')
    except BrokenPipeError:
        pass
    finally:
        try:
            cmus_process.terminate()
        except OSError:
            try:
                cmus_process.kill()
            except OSError:
                pass

def main(port=None, music_folder='musi/'):
    """
    Main function.
    :param int port: port where the server will be
    :param str music_folder: directory in which the music is
    """
    # Create a new process in which execute cmus
    try:
        import subprocess
        cmus_process = subprocess.Popen(args=["cmus"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except Exception as err:
        print('Impossible to open a new cmus instance: {}'.format(err))
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
                    # again
                    time.sleep(1)
                    continue 
                else:
                    print('Impossible to connect to cmus. Exiting the program...')
                    exit_cmus(cmus, cmus_process)
                    sys.exit(1)

        # Get the songs we will play
        import music_extractor
        if not(music_extractor.MusicExtractor(music_folder).songs_list):
            print("There aren't any songs in the chosen directory. Exiting program... ")
            exit_cmus(cmus, cmus_process)
            sys.exit(1)

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
        exit_cmus(cmus, cmus_process)

if __name__ == '__main__':
    # We can choose the port where we will have
    # our app running from the console
    if len(argv) == 1:  
        port = None
    elif len(argv) == 2:
        try:
            port = int(argv[1])
        except ValueError as err:
            print('Invalid parameter: {}'.format(err))
            print('Assigning default port')
            port = None
    else:
        print('Invalid number of parameters. Assigning default port')
        port = None
    main(port)
    