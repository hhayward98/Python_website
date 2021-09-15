from datetime import datetime
import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db 
from sqlalchemy.sql.expression import select, exists
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

app.config['SECRET_KEY'] = b'I\x97r\x9e\xd2\xe5\xf6\xd7\x07\x84B\x17D\x04^\xd1\x17O\xd2\xb2cI2\xaa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite///C:/Users/HHaut/GITHUB/Python_website/app/appDatabase.db'


class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	password_hash = db.Column(db.String(128))


	def set_password(self, password):
		self.password_hash = generate_password_hash(password)


	def check_password(self, password):
		return check_password_hash(self.password_hash, password)


	def __repr__(self):
		return '<User {}>'.format(self.username)


