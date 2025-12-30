import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app  = Flask(__name__)
app.secret_key="ahgfsdkhadsn"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/studentdb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 3
cloudinary.config(
    cloud_name="dfjad5nwf",
    api_key="837779219761189",
    api_secret="uReczUlvmiTpCW6NG5sWxhrsE7Q",
    secure=True
)

db = SQLAlchemy(app)
login=LoginManager(app)

