from flask import Flask

app = Flask(__name__)

app.secret_key = "hello_i_am_a_secret"