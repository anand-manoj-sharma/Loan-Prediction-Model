#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 23:01:56 2019

@author: admin
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pyrebase as pb
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  

config = {
    "apiKey": "AIzaSyCEEpwEB20Plnz9VMyIJqm2OL7H-5hpeaM",
    "authDomain": "stproject-81d33.firebaseapp.com",
    "databaseURL": "https://stproject-81d33.firebaseio.com",
    "projectId": "stproject-81d33",
    "storageBucket": "stproject-81d33.appspot.com",
    "messagingSenderId": "645228603641",
    "appId": "1:645228603641:web:250a07a5c6f99289231a28"
  };
      
i=0        
while i<100:
    i=i+1
    print(i)
    firebase=pb.initialize_app(config)
    
    db=firebase.database()
    appinc=db.child("Details").child("appinc").get()
    coappinc=db.child("Details").child("coappinc").get()
    dependents=db.child("Details").child("dependents").get()
    education=db.child("Details").child("education").get()
    gender=db.child("Details").child("gender").get()
    loanamount=db.child("Details").child("loanamount").get()
    loanterm=db.child("Details").child("loanterm").get()
    marital=db.child("Details").child("marital").get()
    propert=db.child("Details").child("property").get()
    repay=db.child("Details").child("repay").get()
    selfemp=db.child("Details").child("selfemp").get()
    #aa=selfemp.val()
    #print(type(aa))
    loanamount_float=float(loanamount.val())
    loanamount_float_log=np.log(loanamount_float)
    #print(loanamount_float_log)
    #loanamount_log=np.log(loanamount.val())   
    if(repay.val()=='Yes'):
         history=0
    else:
        history=1  
    data={
          'Gender':[gender.val()],
          'Married':[marital.val()],
          'Dependents':[dependents.val()],
          'Education':[education.val()],
          'Self_Employed':[selfemp.val()],
          'ApplicantIncome':[int(appinc.val())],
          'CoapplicantIncome':[int(coappinc.val())],
          'LoanAmount':[float(loanamount.val())],
          'Loan_Amount_Term':[float(loanterm.val())],
          'Credit_History':[float(history)],
          'Property_Area':[propert.val()]
          } 
    import pandas as pd
    train=pd.read_csv('clean_train.csv')
    test=pd.read_csv('clean_test.csv')   
    train = train.drop('Loan_ID', axis=1)
    test = test.drop('Loan_ID', axis=1)
    train = train.drop(train.columns[0], axis=1)
    test = test.drop(test.columns[0], axis=1)
    #print(train.columns)
    #print(test.columns)
    X = train.drop('Loan_Status', 1)
    y = train.Loan_Status
    df=pd.DataFrame(data)
    df['LoanAmount_log']=loanamount_float_log
    #print(df.info())
    test=test.append(df,ignore_index=True)
    #print(test.info())
    X = pd.get_dummies(X)
    train = pd.get_dummies(train)
    test = pd.get_dummies(test)
    #print(test.info())
    #print(train.info())
    #print(X.info())
    from sklearn.model_selection import train_test_split
    x_train, x_cv, y_train, y_cv = train_test_split(X, y, test_size=0.3, random_state=0)
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score
    model = LogisticRegression()
    model.fit(x_train, y_train)
    pred_cv = model.predict(x_cv)
    print(accuracy_score(y_cv, pred_cv))
    pred_test = model.predict(test)
    result=pred_test[-1]
    if(result=='Y'):
        print('YESSSSSSS')
        result='Y'
    else:
        result='N'
        print('NOOOOO')    
    db.child("Details").child("result").set(result)
