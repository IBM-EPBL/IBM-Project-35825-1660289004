from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests
import json
import pickle
model = pickle.load(open('university.pkl','rb'))
import pyrebase
API_KEY = "w7wZ3NDUKJjLg9ulwEFwDCKCnOurNNLrzp3gZ-SNrbGO"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token',
data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
config = {
"apiKey": "AIzaSyBLcGYGA82pCAHW4xKjgDYv_bsnEJEgo1E",
"authDomain": "universityadmitpredictor.firebaseapp.com",
"projectId": "universityadmitpredictor",
"storageBucket": "universityadmitpredictor.appspot.com",
"messagingSenderId": "938493164189",
"databaseURL":
"https://console.firebase.google.com/u/0/project/universityadmitpredictor/database/
universityadmitpredictor-default-rtdb/data/~2F",
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
model = pickle.load(open('university.pkl','rb'))
app = Flask(__name__)
@app.route('/',methods=['GET','POST'])
def homepage():
if request.method == 'POST':
unsuccessful = 'Please check your credentials'
email = request.form['name']
password = request.form['pass']
try:
auth.sign_in_with_email_and_password(email, password)
return render_template('index.html')
except:
auth.create_user_with_email_and_password(email,password)
auth.sign_in_with_email_and_password(email, password)
return render_template('index.html')
return render_template('login.html')
@app.route('/predict', methods=['GET', 'POST'])
def predict():
if request.method == 'POST':
gre = request.form['gre']
toefl = request.form['toefl']
universityNumber = request.form['universityNumber']
sop = request.form['sop']
lor = request.form['lor']
cgpa = request.form['cgpa']
research = request.form['research']
y_pred = [[gre, toefl, universityNumber, sop, lor, cgpa, research]]
payload_scoring = {"input_data": [
{"field": [["GRE Score", "TOEFL Score", "University Rating", "SOP",
"LOR ", "CGPA", "Research"]],
"values": y_pred}]}
response_scoring =
requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/67f91885-c382-4d
94-9b23-60bbc3f65a47/predictions?version=2022-11-18',json=payload_scoring,headers={
'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
print(response_scoring.json())
predictions = response_scoring.json()
output = predictions['predictions'][0]['values'][0][0]
print(output)
if output == 'Yes':
return render_template('chance.html')
if output == 'No':
return render_template('Nochance.html')
return render_template('index.html')
@app.route('/index.html',methods=['GET', 'POST'])
def index():
return render_template('index.html')
@app.route('/about.html')
def about():
return render_template('about.html')
if __name__ == '__main__':
app.run(debug=True)