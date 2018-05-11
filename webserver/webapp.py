from flask import Flask, render_template

class MusicControllerWeb(object):
    """
    This class handles the web that is meant to be
    use for our application
    """
    def __init__(self, name):
        """
        Constructor for the class. It initializes the Flask
        object and renders the web
        :param str name: the name for the app
        """
        super(MusicControllerWeb, self).__init__()
        self.app = Flask(
            name, template_folder="webserver/templates", static_folder="webserver/static"
        )
        self.render_web()

    def render_web(self):
        """
        Render the domains the web will use
        """
        @self.app.route('/')
        def index():
            return render_template('mainpage.html')