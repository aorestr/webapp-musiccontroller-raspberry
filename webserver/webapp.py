from flask import Flask, render_template, request, jsonify
import json

class MusicControllerWeb(object):
    """
    This class handles the web that is meant to be
    used for our application

    :param str name: the name for the app
    :param PyCmus cmus: the cmus handler
    """
    def __init__(self, name, cmus, songs):
        """
        Constructor for the class. It initializes the Flask
        object and renders the web
        """
        super(MusicControllerWeb, self).__init__()
        # Flask main method
        self.app = Flask(
            name, template_folder="webserver/templates", static_folder="webserver/static"
        )
        # cmus controller
        self.cmus = cmus
        # Songs information
        self.songs = songs
        # Songs status. It stores local info.
        # It's easier, faster and less painful 
        # than ask cmus constantly
        self.status = {
            'current_song': 0,
            'playing': False
        }
        # Let's render our web
        self._render_web()

    def _render_web(self):
        """
        Render the domains the web will use
        """

        @self.app.route('/')
        def index():
            return render_template(
                'mainpage.html', 
                is_playing=self.status['playing'], 
                songs = self.songs
            )

        @self.app.route('/_post_data', methods = ['POST'])
        def worker():
            jsonData = request.get_json()
            self._post_handler(jsonData)
            return jsonify(success=True, data=self.status)
            
    def _post_handler(self, jsonData):
        """
        It uses the data the server has received from the client
        and translate it into orders for cmus

        :param lst jsonData: the dictionary with the data
        """

        # Buttons implemented on the webapp
        buttons = {
            1: 'player',
            2: 'prev',
            3: 'next'
        }

        btn_clicked = jsonData[0]['button']
        try:
            if btn_clicked == buttons[1]:
                if self.status['playing'] is True:
                    self.cmus.player_pause()
                else:
                    self.cmus.player_play_file(
                        self.songs.songs_list[self.status['current_song']][0]
                    )
                self.status['playing'] = not(self.status['playing'])
            elif btn_clicked == buttons[2]:
                if self.status['current_song'] > 0:
                    self.status['current_song'] -= 1
                self.cmus.player_play_file(
                    self.songs.songs_list[self.status['current_song']][0]
                )
            elif btn_clicked == buttons[3]:
                if self.status['current_song'] < self.songs.num_songs:
                    self.status['current_song'] += 1
                self.cmus.player_play_file(
                    self.songs.songs_list[self.status['current_song']][0]
                )

                
        except BrokenPipeError as err:
            MusicControllerWeb._cmus_connection_failed(err)

    @staticmethod
    def _cmus_connection_failed(err):
        """
        We call this method if the connection with
        cmus breaks
        """
        print('Connection with cmus has been closed: {}'.format(err))
        try:
            print('Closing server',end='')
            MusicControllerWeb.shutdown_server()
            print('ok')
        except Exception as err2:
            from sys import exit
            print('\nSome problem occured: {}'.format(err2))
            exit('Exiting program...')

    @staticmethod
    def shutdown_server():
        """
        Shutdown the werkzeug server we have opened with Flask. It's used
        when the connection with cmus is died
        """
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()