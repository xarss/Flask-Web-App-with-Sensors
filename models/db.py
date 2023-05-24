from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
instance = "mysql+pymysql://chico:chico@localhost:3306/homeautomation"
#instance = "sqlite:///restaurant"