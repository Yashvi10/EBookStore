# Author Saloni Raythatha
# For learning purpose of python and utilize AWS services I have referred "https://aws.amazon.com/getting-started/" and "https://docs.python.org/3/"
# Have taken bookstore image from https://www.istockphoto.com/photos/bookstore */

from flask import Flask, render_template, redirect, url_for, request
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import sys
import cgi
import cgitb
app=Flask(__name__)

# Author Saloni Raythatha
# Login and Registration part of the application
@app.route('/registration', methods=['GET', 'POST'])
def register_login():
    if request.method == 'POST':
        if request.form.get("register_btn"):
            try:
                client = boto3.client("cognito-idp", region_name="us-east-1")
                client.sign_up(
                    ClientId='osdgke53n8m68qujsp2vocl01',
                    Username=request.form['email'],
                    Password=request.form['password'],
                    UserAttributes=[{"Name": "email", "Value": request.form['email']}], )
                print("======= User created")
                return render_template('display_book_results_all_books.html')
            except ClientError as e:
                if e.response['Error']['Code'] == 'EntityAlreadyExists' or e.response['Error'][
                    'Code'] == 'UsernameExistsException':
                    return render_template('/index.html', error="User already exists - Do login instead")
                else:
                    print(6)
                    error = "Unexpected error"
                    print("Unexpected error: %s" % e)
                    return render_template('/index.html', error=error)
        elif request.form.get("login_btn"):
            try:
                print(1)
                client = boto3.client("cognito-idp", region_name="us-east-1")
                auth_data = {'USERNAME': request.form['email'], 'PASSWORD': request.form['password']}
                print(auth_data)
                client.initiate_auth(
                    AuthFlow='USER_PASSWORD_AUTH',
                    AuthParameters=auth_data,
                    ClientId='osdgke53n8m68qujsp2vocl01')
                return redirect(url_for('display_book_results_all_books'))
            except ClientError as e:
                print(3)
                if e.response['Error']['Code'] == 'EntityAlreadyExists' or e.response['Error'][
                    'Code'] == 'UsernameExistsException':
                    error = "User already exists - Do login instead"
                    print(4)
                    print("======= User already exists")
                elif e.response['Error']['Code'] == 'UserNotConfirmedException':
                    # this is fine
                    return redirect(url_for('display_book_results_all_books'))
                else:
                    error = "Unexpected error"
                    print(5)
                    print("===== Unexpected error: %s" % e)
                return render_template('/index.html', error=error)
    return render_template('/index.html')

# Author Saloni Raythatha
# User initially sees the index port
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
            return render_template('index.html', error=error)
        else:
            client = boto3.client("cognito-idp", region_name="us-east-1")
            response = client.sign_up(
                ClientId='osdgke53n8m68qujsp2vocl01',
                Username=email,
                Password=password,
                UserAttributes=[{"Name": "email", "Value": email}], )
            print(response)
            return render_template('index.html')
    else:
        return render_template('index.html')

# Author Saloni Raythatha
# Based on the search query user is redirected to display_book_results if there is matching content
@app.route('/display_book_results.html', methods=['GET', 'POST'])
def display_results():
    error = None
    dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id='AKIAVVCE6YC6UVS63U5J',
                    aws_secret_access_key='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',
                    region_name='us-east-1')

    table = dynamodb.Table('library_storage2')
    response = table.query(KeyConditionExpression=Key('title').eq(request.form['search'])
    )

    items = response['Items']
    if len(items) > 0:
        return render_template('display_book_results.html', error=error, items=items)
    else:
        return render_template('index.html', error="No Results Found for Search term " + request.form['search'])


# Author Saloni Raythatha
@app.route('/display_book_results_all_books.html', methods=['GET', 'POST'])
def display_book_results_all_books():
    error = None
    dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id='AKIAVVCE6YC6UVS63U5J',
                    aws_secret_access_key='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',
                    region_name='us-east-1')

    table = dynamodb.Table('library_storage2')
    response = table.scan()
    return render_template('display_book_results_all_books.html', error=error, items=response['Items'])


# run the application
if __name__ == '__main__':
    app.run(debug=True)