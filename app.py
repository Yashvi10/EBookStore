#Author Saloni Raythatha

from flask import Flask, render_template, redirect, url_for, request
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import sys
import cgi
import cgitb

app=Flask(__name__)




# connection established with AWS congnito from python
@app.route('/registration', methods=['GET', 'POST'])
def login():
    print(0.0)
    if request.method == 'POST':
        if request.form.get("register_btn"):
            print(1)
            try:
                print(2)
                client = boto3.client("cognito-idp", region_name="us-east-1")
                client.sign_up(
                    ClientId='osdgke53n8m68qujsp2vocl01',
                    Username=request.form['email'],
                    Password=request.form['password'],
                    UserAttributes=[{"Name": "email", "Value": request.form['email']}], )
                print("======= User created")
                print(3)
                return render_template('display_book_results.html')
            except ClientError as e:
                print(4)
                if e.response['Error']['Code'] == 'EntityAlreadyExists' or e.response['Error']['Code'] == 'UsernameExistsException':
                    print(5)
                    error = "User already exists - Do login instead"
                    print("======= User already exists")
                else:
                    print(6)
                    error = "Unexpected error"
                    print("===== Unexpected error: %s" % e)
                return render_template('/index.html', error=error)

        elif request.form.get("login_btn"):
            print(7)
            return render_template('/display_book_results.html')




#Route for handling the login page logic
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

@app.route('/display_book_results.html', methods=['GET', 'POST'])
def display_results():
    error = None
    print(1)
    dynamodb = boto3.resource('dynamodb',
                              aws_access_key_id='AKIAVVCE6YC6UVS63U5J',
                              aws_secret_access_key='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',
                              region_name='us-east-1')

    table = dynamodb.Table('library_storage2')
    response = table.query(
        KeyConditionExpression=Key('title').eq(request.form['search'])
    )
    items = response['Items']
    print(items)
    data = response['Items']
    print(response)

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    return render_template('display_book_results.html', error=error, items=items)

if __name__ == '__main__':
    app.run(debug=True)