from flask_app import app
from flask_app.controllers import ingredients
from flask_app.controllers import recipes
from flask_app.controllers import users

# from terminal navigate to directory of project
# run "pipenv shell"
# run "python server.py"
# (note: may need to rerun "pipenv install flask" first)
# navigate to localhost://5000

if __name__ == "__main__":
    app.run(debug=True)