# How the User Authentication System Works

## SQLite database
### - connects to app through SQLAlchemy
### - contains a "user" table
### - each user has a username and password field

## Registration Page
### - has a form where users input a username and password to create an account
### - when users submits account creation information, their information is added into the user table in the database

## Login Page
### - has a form where users input their information to log in
### - when a user submits a login request, the app tries to find the username in the database
### - if username matches, then attempts to match the password
### - if the passsword is correct, the user get logged in and redirected to the dashboard page