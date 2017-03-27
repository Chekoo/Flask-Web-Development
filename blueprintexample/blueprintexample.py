from flask import Flask
from simple_page.simple_page import simple_page

app = Flask(__name__)
app.register_blueprint(simple_page)
app.register_blueprint(simple_page, url_prefix='/pages')

if __name__ == '__main__':
    app.run()