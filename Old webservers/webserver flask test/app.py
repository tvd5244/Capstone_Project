# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request
import UserAccountSet
import re

# create the application object
app = Flask(__name__)

# use decorators to link the function to a url
@app.route('/login')
def home():
    return render_template('login.html')  # return a string
	
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	#error = None
	#if request.method =="POST":
	#	if request.form['password'] != request.form['confirm_password']:
	#		error = 'Confirmation password is different from entered password!'
	#	elif re.match(r"[a-z]{3}[0-9]{4}@psu\.edu", request.form['username']) is None:
	#		error = 'Email must be a PSU email!'
	#	elif len(request.form['password']) < 8:
	#		error = 'Password must be at least 8 characters!'
	#	else:
	#		user = UserAccountSet.UserAccount.create(request.form['username'], request.form['password'])
	#		user.commit()
	#		return redirect(url_for('home'))
	return render_template('signup.html')
	

#@app.route('/welcome')
#def welcome():
#    return render_template('welcome.html')  # render a template
	
# Route for handling the login page logic
#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    error = None
#    if request.method == 'POST':
#        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
#            error = 'Invalid Credentials. Please try again.'
#        else:
#            return redirect(url_for('home'))
#    return render_template('login.html', error=error)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)