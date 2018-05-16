#!./venv/bin/python3

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

def init_cmus(cmus, music_folder):
    """
    Stop the player (in case is playing any song),
    clear the environment (this is not necessary actually)
    and add the music within the folder we chose
    """
    cmus.send_cmd('player-stop\n')
    cmus.send_cmd('clear\n')
    cmus.send_cmd('add {}\n'.format(music_folder))

def main(port=None, music_folder='music/'):
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
                print('Trying to connect to cmus... ', end='')
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
                    print('\nImpossible to connect to cmus. Exiting the program...')
                    exit_cmus(cmus, cmus_process)
                    sys.exit(1)
        print('ok\n')

        # Get the songs we will play
        import music_extractor
        songs = music_extractor.MusicExtractor(music_folder)
        if not(songs.num_songs):
            print("There aren't any songs in the chosen directory. Exiting program... ")
            exit_cmus(cmus, cmus_process)
            sys.exit(1)
        # 'Reboot' cmus
        init_cmus(cmus, songs.music_folder)
        # Open the web server
        try:
            from webserver.webapp import MusicControllerWeb
            flask_object = MusicControllerWeb(__name__, cmus, songs)
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
        # We delete the directory with the songs' covers within
        songs.del_covers_folder()
        # Before leaving the program, we close
        # the fork with cmus
        exit_cmus(cmus, cmus_process)

if __name__ == '__main__':
    # We can choose the port where we will have
    # our app running from the console
    if len(sys.argv) == 1:  
        port = None
    elif len(sys.argv) == 2:
        try:
            port = int(sys.argv[1])
        except ValueError as err:
            print('Invalid parameter: {}'.format(err))
            print('Assigning default port')
            port = None
    else:
        print('Invalid number of parameters. Assigning default port')
        port = None
    main(port)
    