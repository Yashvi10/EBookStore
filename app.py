#Author Saloni Raythatha

from flask import Flask, render_template, redirect, url_for, request
import boto3

app=Flask(__name__)

# connection established with AWS congnito from python
@app.route('/login', methods=['GET', 'POST'])
def login():
    print("0")

    error = None
    if request.method == 'POST':
        client = boto3.client("cognito-idp", region_name="us-east-1")
        response = client.sign_up(
            ClientId='osdgke53n8m68qujsp2vocl01',
            Username=request.form['email'],
            Password=request.form['password'],
            UserAttributes=[{"Name": "email", "Value": request.form['email']}], )
        print(response)
    return render_template('display_book_results.html', error=error)


#Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            client = boto3.client("cognito-idp", region_name="us-east-1")
            response = client.sign_up(
                ClientId='osdgke53n8m68qujsp2vocl01',
                Username=email,
                Password=password,
                UserAttributes=[{"Name": "email", "Value": email}], )
            print(response)
            return redirect(url_for('home'))
    return render_template('index.html', error=error)



@app.route('/display_book_results.html', methods=['GET'])
def display_results():
    error = None
    return render_template('display_book_results.html', error=error)

def display():
    return "This is about page";
    return render_template('display_book_results.html', error=error)
app.add_url_rule("/display_book_results", "display", display)

if __name__ == '__main__':
    app.run(debug=True)