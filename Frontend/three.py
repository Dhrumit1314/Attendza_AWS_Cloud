from flask import Flask, render_template, request
import sqlite3
from datetime import datetime
import boto3

dynamodb = boto3.client('dynamodb', region_name = 'us-east-1')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', selected_date='', no_data=False)

@app.route('/attendance', methods=['POST'])
def attendance():
    selected_date = request.form.get('selected_date')
    selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
    formatted_date = selected_date_obj.strftime('%Y-%m-%d')
    
    attendance = dynamodb.scan(
            TableName='attendence',
            FilterExpression='#date = :date_val',
            ExpressionAttributeNames={
                '#date': 'date'
            },
            ExpressionAttributeValues={
                ':date_val': {'S': formatted_date}
            }
        )
    
    attendance_data = attendance['Items']
    
    if len(attendance_data) == 0:
        return render_template('index.html', selected_date=selected_date, no_data=True)

    return render_template('index.html', selected_date=selected_date, attendance_data=attendance_data)

if __name__ == '__main__':
    app.run(debug=True)