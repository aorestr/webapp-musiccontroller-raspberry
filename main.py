#!/usr/bin/python3

def main():
    """
    Main function of the program
    """

    # Import the class with the methods to use
    # cmus remotely
    from pycmus import remote
    from pycmus import exceptions

    try:
        cmus = remote.PyCmus()
    except exceptions.CmusNotRunning:
        pass
    else:
        print(cmus.status())
        cmus.player_pause()


#################################################################3

# Abrimos el programa si se ha ejecutado desde este fichero
if __name__ == "__main__":
    from sys import argv
    try:
        main()
    except ValueError as e:
        print(e)