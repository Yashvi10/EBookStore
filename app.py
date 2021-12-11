# Author Saloni Raythatha
import json
import random
from json import dump

from flask import Flask, render_template, redirect, url_for, request
import boto3
from boto3.dynamodb.conditions import Key

app = Flask(__name__)


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


# Route for handling the login page logic
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


@app.route('/rent', methods=['GET', 'POST'])
def rent():
    dynamodb = boto3.resource('dynamodb',
                              aws_access_key_id='ASIA2H253BUSTJKE2HJG',
                              aws_secret_access_key='2274XxOgNlSjMtJuOC1AmHeWZ1lK5KlHCi/q3ULn',
                              aws_session_token='FwoGZXIvYXdzEDMaDEQKDmXo3xraAG1h3CLIATWx4L9BkfySmZn8Qh559c9ZFPmI3oUclwoLLt2iBt1cRFF44krRCD3r0iuxRO88RitmJsDzi0wewaczP5ay+FDq72OQ2zvVZ0AcCWM40hZtx1brnNIuImLF/Bnqf0WdlfjqI04LfwcXWxM2ukzGE46Ot6Gajnw3AQ7RDO8YV2CNhqu0FFiMfGtkyQq4GiA62Qz1ByQVmkgx+1TnYLno0oN2t8neVkD/WsiNKnrungKiHEGvh8IHEZKsljKbp0zgioPh9/yL4XF4KLH8z40GMi2QCsktbI/kjiHU3BNwCKY6Am+yUIkxAKqU/XOkaGAROpSVEVRJ1aQUWWXFZeA=',
                              region_name='us-east-1')
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:5000")

    table = dynamodb.Table('bookManagement')
    scan_kwargs = {
        'FilterExpression': Key('quantity').between(1, 100),
        'ProjectionExpression': "bookName, authorName, genre",
    }
    done = False
    start_key = None
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)
        response.get('Items', [])
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None
    response = table.scan(**scan_kwargs)

    return render_template('rent.html', value=response['Items'], value1=len(response['Items']))


@app.route('/rentConfirmation', methods=['GET', 'POST'])
def rentConfirmation():
    dynamodb = boto3.resource('dynamodb',
                              aws_access_key_id='ASIA2H253BUSTJKE2HJG',
                              aws_secret_access_key='2274XxOgNlSjMtJuOC1AmHeWZ1lK5KlHCi/q3ULn',
                              aws_session_token='FwoGZXIvYXdzEDMaDEQKDmXo3xraAG1h3CLIATWx4L9BkfySmZn8Qh559c9ZFPmI3oUclwoLLt2iBt1cRFF44krRCD3r0iuxRO88RitmJsDzi0wewaczP5ay+FDq72OQ2zvVZ0AcCWM40hZtx1brnNIuImLF/Bnqf0WdlfjqI04LfwcXWxM2ukzGE46Ot6Gajnw3AQ7RDO8YV2CNhqu0FFiMfGtkyQq4GiA62Qz1ByQVmkgx+1TnYLno0oN2t8neVkD/WsiNKnrungKiHEGvh8IHEZKsljKbp0zgioPh9/yL4XF4KLH8z40GMi2QCsktbI/kjiHU3BNwCKY6Am+yUIkxAKqU/XOkaGAROpSVEVRJ1aQUWWXFZeA=',
                              region_name='us-east-1')
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:5000")

    table = dynamodb.Table('userDetails')
    response = table.query(
        KeyConditionExpression=Key('libraryid').eq("1")
    )
    init_credits = int(response['Items'][0]['credits'])
    redeemed_credits = init_credits - 1
    if redeemed_credits > 0:
        table2 = dynamodb.Table('transaction')
        response2 = table2.put_item(
            Item={
                'transactionid': random.randint(1, 100),
                'type': "rent",
                'bookName': request.form['bookName']
            }
        )
        table4 = dynamodb.Table('bookManagement')
        response4 = table4.query(
            KeyConditionExpression=Key('bookName').eq(request.form['bookName'])
        )
        quantity = int(response4['Items'][0]['quantity'])
        quantity = quantity - 1
        table3 = dynamodb.Table('bookManagement')
        response3 = table3.update_item(
            Key={
                'bookName': request.form['bookName']
            }, UpdateExpression="set quantity=:q",
            ExpressionAttributeValues={
                ':q': quantity
            },
            ReturnValues="UPDATED_NEW"
        )
        if response2:
            table3 = dynamodb.Table('userDetails')
            response3 = table3.put_item(
                Item={
                    'libraryid': "1",
                    'credits': redeemed_credits
                }
            )
        jsonstring = "You will receive an email notification as confirmation of using this service and $1 would be deducted from your library card credits! YOUR REMAINING CREDITS ARE: " + str(
            redeemed_credits) + " Please return the book within 30 days which is the rent period!"
        return json.dumps(jsonstring)
    else:
        jsonstring = "Sorry you dont have sufficient credits in your account! You just have " + str(
            init_credits) + "left in yu=our account!"
        return json.dumps(jsonstring)


@app.route('/buy', methods=['GET', 'POST'])
def buy():
    dynamodb = boto3.resource('dynamodb',
                              aws_access_key_id='ASIA2H253BUSTJKE2HJG',
                              aws_secret_access_key='2274XxOgNlSjMtJuOC1AmHeWZ1lK5KlHCi/q3ULn',
                              aws_session_token='FwoGZXIvYXdzEDMaDEQKDmXo3xraAG1h3CLIATWx4L9BkfySmZn8Qh559c9ZFPmI3oUclwoLLt2iBt1cRFF44krRCD3r0iuxRO88RitmJsDzi0wewaczP5ay+FDq72OQ2zvVZ0AcCWM40hZtx1brnNIuImLF/Bnqf0WdlfjqI04LfwcXWxM2ukzGE46Ot6Gajnw3AQ7RDO8YV2CNhqu0FFiMfGtkyQq4GiA62Qz1ByQVmkgx+1TnYLno0oN2t8neVkD/WsiNKnrungKiHEGvh8IHEZKsljKbp0zgioPh9/yL4XF4KLH8z40GMi2QCsktbI/kjiHU3BNwCKY6Am+yUIkxAKqU/XOkaGAROpSVEVRJ1aQUWWXFZeA=',
                              region_name='us-east-1')
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:5000")

    table = dynamodb.Table('bookManagement')
    scan_kwargs = {
        'FilterExpression': Key('quantity').between(1, 100),
        'ProjectionExpression': "bookName, authorName, genre",
    }
    done = False
    start_key = None
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)
        response.get('Items', [])
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None
    response = table.scan(**scan_kwargs)

    return render_template('buy.html', value=response['Items'], value1=len(response['Items']))


@app.route('/buyConfirmation', methods=['GET', 'POST'])
def buyConfirmation():
    dynamodb = boto3.resource('dynamodb',
                              aws_access_key_id='ASIA2H253BUSTJKE2HJG',
                              aws_secret_access_key='2274XxOgNlSjMtJuOC1AmHeWZ1lK5KlHCi/q3ULn',
                              aws_session_token='FwoGZXIvYXdzEDMaDEQKDmXo3xraAG1h3CLIATWx4L9BkfySmZn8Qh559c9ZFPmI3oUclwoLLt2iBt1cRFF44krRCD3r0iuxRO88RitmJsDzi0wewaczP5ay+FDq72OQ2zvVZ0AcCWM40hZtx1brnNIuImLF/Bnqf0WdlfjqI04LfwcXWxM2ukzGE46Ot6Gajnw3AQ7RDO8YV2CNhqu0FFiMfGtkyQq4GiA62Qz1ByQVmkgx+1TnYLno0oN2t8neVkD/WsiNKnrungKiHEGvh8IHEZKsljKbp0zgioPh9/yL4XF4KLH8z40GMi2QCsktbI/kjiHU3BNwCKY6Am+yUIkxAKqU/XOkaGAROpSVEVRJ1aQUWWXFZeA=',
                              region_name='us-east-1')
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:5000")

    table = dynamodb.Table('userDetails')
    response = table.query(
        KeyConditionExpression=Key('libraryid').eq("1")
    )
    init_credits = int(response['Items'][0]['credits'])
    redeemed_credits = init_credits - 1
    if redeemed_credits > 0:
        table2 = dynamodb.Table('transaction')
        response2 = table2.put_item(
            Item={
                'transactionid': random.randint(1, 100),
                'type': "buy",
                'bookName': request.form['bookName']
            }
        )
        table4 = dynamodb.Table('bookManagement')
        response4 = table4.query(
            KeyConditionExpression=Key('bookName').eq(request.form['bookName'])
        )
        quantity = int(response4['Items'][0]['quantity'])
        quantity = quantity - 1
        table3 = dynamodb.Table('bookManagement')
        response3 = table3.update_item(
            Key={
                'bookName': request.form['bookName']
            }, UpdateExpression="set quantity=:q",
            ExpressionAttributeValues={
                ':q': quantity
            },
            ReturnValues="UPDATED_NEW"
        )
        if response2:
            table3 = dynamodb.Table('userDetails')
            response3 = table3.put_item(
                Item={
                    'libraryid': "1",
                    'credits': redeemed_credits
                }
            )
        jsonstring = {
            "message": "You will receive an email notification as confirmation of using this service and $3 would be deducted from your library card credits! YOUR REMAINING CREDITS ARE: " + str(
                redeemed_credits) + "Hope you would enjoy reading this book!"}
        return json.dumps(jsonstring)
    else:
        jsonstring = "Sorry you dont have sufficient credits in your account! You just have " + str(
            init_credits) + "left in your account!"
        return json.dumps(jsonstring)


@app.route('/donate', methods=['GET', 'POST'])
def donate():
    return render_template('donate.html')


@app.route('/donateConfirmation', methods=['GET', 'POST'])
def donateConfirmation():
    dynamodb = boto3.resource('dynamodb',
                              aws_access_key_id='ASIA2H253BUSTJKE2HJG',
                              aws_secret_access_key='2274XxOgNlSjMtJuOC1AmHeWZ1lK5KlHCi/q3ULn',
                              aws_session_token='FwoGZXIvYXdzEDMaDEQKDmXo3xraAG1h3CLIATWx4L9BkfySmZn8Qh559c9ZFPmI3oUclwoLLt2iBt1cRFF44krRCD3r0iuxRO88RitmJsDzi0wewaczP5ay+FDq72OQ2zvVZ0AcCWM40hZtx1brnNIuImLF/Bnqf0WdlfjqI04LfwcXWxM2ukzGE46Ot6Gajnw3AQ7RDO8YV2CNhqu0FFiMfGtkyQq4GiA62Qz1ByQVmkgx+1TnYLno0oN2t8neVkD/WsiNKnrungKiHEGvh8IHEZKsljKbp0zgioPh9/yL4XF4KLH8z40GMi2QCsktbI/kjiHU3BNwCKY6Am+yUIkxAKqU/XOkaGAROpSVEVRJ1aQUWWXFZeA=',
                              region_name='us-east-1')
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:5000")

    table = dynamodb.Table('donatedBooks')
    response = table.put_item(
        Item={
            'libraryid': request.form['libraryid'],
            'bookName': request.form['bookName'],
            'authorName': request.form['authorName'],
            'genre': request.form['genre']
        }
    )
    table = dynamodb.Table('bookManagement')
    response = table.put_item(
        Item={
            'bookName': request.form['bookName'],
            'authorName': request.form['authorName'],
            'genre': request.form['genre'],
            'quantity': 1
        }
    )
    if response:
        jsonstring = {"message": "Thank you for donating book and using our service!"}
        return json.dumps(jsonstring)
    else:
        jsonstring = {"message": "There is some kind of error occurred!"}
        return json.dumps(jsonstring)


@app.route('/request', methods=['GET', 'POST'])
def requestBook():
    return render_template('request.html')


@app.route('/requestConfirmation', methods=['GET', 'POST'])
def requestConfirmation():
    dynamodb = boto3.resource('dynamodb',
                              aws_access_key_id='ASIA2H253BUSTJKE2HJG',
                              aws_secret_access_key='2274XxOgNlSjMtJuOC1AmHeWZ1lK5KlHCi/q3ULn',
                              aws_session_token='FwoGZXIvYXdzEDMaDEQKDmXo3xraAG1h3CLIATWx4L9BkfySmZn8Qh559c9ZFPmI3oUclwoLLt2iBt1cRFF44krRCD3r0iuxRO88RitmJsDzi0wewaczP5ay+FDq72OQ2zvVZ0AcCWM40hZtx1brnNIuImLF/Bnqf0WdlfjqI04LfwcXWxM2ukzGE46Ot6Gajnw3AQ7RDO8YV2CNhqu0FFiMfGtkyQq4GiA62Qz1ByQVmkgx+1TnYLno0oN2t8neVkD/WsiNKnrungKiHEGvh8IHEZKsljKbp0zgioPh9/yL4XF4KLH8z40GMi2QCsktbI/kjiHU3BNwCKY6Am+yUIkxAKqU/XOkaGAROpSVEVRJ1aQUWWXFZeA=',
                              region_name='us-east-1')
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:5000")

    table = dynamodb.Table('requestedBooks')
    response = table.put_item(
        Item={
            'libraryid': request.form['libraryid'],
            'bookName': request.form['bookName'],
            'authorName': request.form['authorName'],
            'genre': request.form['genre']
        }
    )
    if response:
        jsonstring = {"message": "Thank you for requesting book and using our service, we will get back to you once "
                                 "we have the book you requested!"}
        return json.dumps(jsonstring)
    else:
        jsonstring = {"message": "There is some kind of error occurred!"}
        return json.dumps(jsonstring)


if __name__ == '__main__':
    app.run(debug=True)
    app.run()
