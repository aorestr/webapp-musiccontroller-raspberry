import os
from tinytag.tinytag import TinyTag

class MusicExtractor(object):
    """
    Class that handles the folder with the music
    we have chosen
    :param str music_folder: path where the music is
    """
    def __init__(self, music_folder):
        super(MusicExtractor, self).__init__()
        self.music_folder = MusicExtractor.music_folder_fullpath(music_folder)
        self.songs_list = self.extract_music()

    @staticmethod
    def music_folder_fullpath(music_folder):
        """
        Gives the absolute path of our music folder
        """
        if(music_folder[-1] != '/'):
            music_folder += '/'
        return '{}/{}'.format(os.path.dirname(os.path.abspath(music_folder)), music_folder)

    def extract_music(self):
        """
        Create a tuple that contains the songs' filename and their info
        :param str music_folder: path of the directory where the music is
        :return resp: The response from cmus from the issued command
        :rtype: tuple
        """

        def song_fullpath(music_folder,filename):
            """
            Extracts the fullpath of a song
            """
            return ('{}{}'.format(music_folder,filename))

        songs = []
        try:
            generator = (f for f in os.listdir(self.music_folder) if os.path.isfile(os.path.join(self.music_folder, f)))
        except (FileNotFoundError, Exception) as err:
            print('Impossible to obtain the songs: {}'.format(err))
        else:
            for song in generator:
                path = song_fullpath(self.music_folder, song)
                try:
                    new_song = TinyTag.get(path, image=True)
                except Exception:
                    try:
                        print('ok')
                        new_song = TinyTag.get(path)
                    except Exception as e: 
                        print('File {} has not a valid format for a song: {}'.format(path, e))
                        new_song = None
                finally:
                    if new_song and (new_song.bitrate and new_song.samplerate and new_song.duration):
                        # Avoid no-song files to be added
                        songs.append((path, new_song))

        return tuple(songs)
