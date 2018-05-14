import os
from tinytag.tinytag import TinyTag

class MusicExtractor(object):
    """
    Class that handles the folder with the music
    we have chosen
    :param str music_folder: path where the music is
    """
    def __init__(self, music_folder, covers_folder='covers/'):
        super(MusicExtractor, self).__init__()
        self.music_folder = MusicExtractor.music_folder_fullpath(music_folder)
        # Get the songs it will be possible to play
        self.songs_list = self.extract_music()
        self.num_songs = len(self.songs_list)
        self.covers_folder = os.path.join('webserver/static', covers_folder)
        # Create a folder with the cover images 
        self.create_imgs()

    @staticmethod
    def music_folder_fullpath(music_folder):
        """
        Gives the absolute path of our music folder
        """
        if(music_folder[-1] != '/'):
            music_folder += '/'
        return '{}'.format( 
                        os.path.join(os.path.dirname(os.path.abspath(music_folder)), music_folder)
                        ) 

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

    def create_imgs(self):
        """
        Create a folder in which store all the cover images
        of the songs we have chosen
        """
        print('Creating image files with the cover of each song... ')
        if not os.path.exists(self.covers_folder):
            os.makedirs(self.covers_folder)
        for i in range(0, self.num_songs):
            try:
                image = self.songs_list[i][1].get_image()
                if image:
                    # We create a file only if the cover is in the file
                    with open('./{}.jpg'.format(os.path.join(self.covers_folder, str(i))), 'wb') as image_file:
                        image_file.write(image)
                else:
                    # No file will be creating in case it's not
                    print('No cover picture in {}'.format(self.songs_list[i][0]))
            except Exception as err:
                print(
                    'Problem extracting the cover for {}: {}'.format(
                                                                self.songs_list[i][0],
                                                                err)
                )
        print('Done!')

    def del_covers_folder(self):
        """
        Remove the folder in which the images are. It's used
        mainly when the server closes
        """
        try:
            # Remove every image
            gen = (
                os.remove(os.path.join(self.covers_folder, f)) 
                for f in os.listdir(self.covers_folder) if os.path.isfile(os.path.join(self.covers_folder, f))
            )
            for _ in gen:
                pass
            # And then the folder itself
            os.rmdir(self.covers_folder)
        except OSError:
            pass     