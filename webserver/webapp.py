from flask import Flask, render_template, request, jsonify
import json

class MusicControllerWeb(object):
    """
    This class handles the web that is meant to be
    used for our application

    :param str name: the name for the app
    :param PyCmus cmus: the cmus handler
    """
    def __init__(self, name, cmus):
        """
        Constructor for the class. It initializes the Flask
        object and renders the web
        """
        super(MusicControllerWeb, self).__init__()
        self.app = Flask(
            name, template_folder="webserver/templates", static_folder="webserver/static"
        )
        self.cmus = cmus
        self._render_web()

    def _render_web(self):
        """
        Render the domains the web will use
        """

        @self.app.route('/')
        def index():
            _cmus_status = None
            try:
                _cmus_status = self.cmus.get_status_dict()
            except BrokenPipeError as err:
                MusicControllerWeb._cmus_connection_failed(err)
            return render_template('mainpage.html', cmus_status=_cmus_status)

        @self.app.route('/_post_data', methods = ['POST'])
        def worker():
            jsonData = request.get_json()
            self._post_handler(jsonData)
            return jsonify(success=True, data=self.cmus.get_status_dict())
            
    def _post_handler(self, jsonData):
        """
        It uses the data the server has received from the client
        and translate it into orders for cmus

        :param lst jsonData: the dictionary with the data
        """

        # Buttons implemented on the webapp
        buttons = {
            1: 'player'
        }

        btn_clicked = jsonData[0]['button']
        try:
            if btn_clicked == buttons[1]:
                if self.cmus.get_status_dict()['status'] == 'playing':
                    self.cmus.player_pause()
                else:
                    self.cmus.player_play()
                
        except BrokenPipeError as err:
            MusicControllerWeb._cmus_connection_failed(err)

    @staticmethod
    def _cmus_connection_failed(err):
        """
        We call this method if the connection with
        cmus breaks
        """
        print('Connection with cmus has been closed: ', end='')
        print(err)
        try:
            print('Closing server',end='')
            MusicControllerWeb.shutdown_server()
            print('ok')
        except Exception as err:
            from sys import exit
            print('Some problem occured: ', end='')
            print(err)
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