from flask import Flask, request, redirect, render_template
import cgi

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too


@app.route("/welcome", methods=['POST'])
def welcome_user():
    # look inside the request to figure out what the user typed
    user = request.form['user_name']
    password = request.form['password']
    verify_password = request.form['verify_password']
    email = request.form['email']

    temp = "&user_name={0}&email={1}".format(user, email)

    # if the user typed nothing at all, redirect and tell them the error
    if (not user) or (user.strip() == ""):
        user_error = "Please enter a username."
        return redirect("/?user_error=" + user_error + temp)
    
    if len(user) < 3 or len(user) > 20:
        user_error = "Usernames should be between 3 and 20 characters."
        return redirect("/?user_error=" + user_error + temp)

    if (not password) or (password.strip() == ""):
        password_error = "Please enter a password."
        return redirect("/?password_error=" + password_error + temp)

    if len(password) < 3 or len(password) > 20:
        password_error = "Passwords should be between 3 and 20 characters."
        return redirect("/?password_error=" + password_error + temp)

    if (not verify_password) or (verify_password.strip() == ""):
        verify_password_error = "Please re-enter your password."
        return redirect("/?verify_password_error=" + verify_password_error + temp)

    if verify_password != password:
        verify_password_error = "Please re-enter your password."
        return redirect("/?verify_password_error=" + verify_password_error + temp)
    
    if (email) and (email.strip() != ""):
        if "@" not in email or "." not in email:
            email_error = "Please enter a valid email address."
            return redirect("/?email_error=" + email_error + temp)
    
        if len(email) < 3 or len(email) > 20:
            email_error = "Emails should be between 3 and 20 characters."
            return redirect("/?email_error=" + email_error + temp)
    
    return render_template('welcome.html', user_name=user)

@app.route("/")
def index():
    encoded_user_error = request.args.get("user_error")
    encoded_password_error = request.args.get("password_error")
    encoded_verify_password_error = request.args.get("verify_password_error")
    encoded_email_error = request.args.get("email_error")
    encoded_user_name = request.args.get("user_name")
    encoded_email = request.args.get("email")

    if encoded_user_name == None:
        encoded_user_name = ""

    if encoded_email == None:
        encoded_email = ""

    return render_template('index.html', 
    user_error=encoded_user_error and cgi.escape(encoded_user_error, quote=True), 
    password_error=encoded_password_error and cgi.escape(encoded_password_error, quote=True),
    verify_password_error=encoded_verify_password_error and cgi.escape(encoded_verify_password_error, quote=True),
    email_error=encoded_email_error and cgi.escape(encoded_email_error, quote=True),
    user_name = encoded_user_name and cgi.escape(encoded_user_name, quote=True),
    email= encoded_email and cgi.escape(encoded_email, quote=True))

app.run()
