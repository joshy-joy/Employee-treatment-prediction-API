from flask import render_template, request
from app import app
import json
import numpy as np
import pandas as pd
from sklearn.externals import joblib
from sklearn.ensemble import ExtraTreesClassifier

#importing model
model = joblib.load('app/models/treatment_model.pkl')
pd.set_option('display.max_columns', None)

#function to encode binary
def encodeYesNo(data, feature):
    data.loc[data[feature] == 'Yes', feature] = 1
    data.loc[data[feature] == 'No', feature ] = 0

#function to process Data
def process_data(data):

    try:
        #preprocessing age--------------------------
        data['Age'] = data['Age'].astype(np.int64)
        data.loc[0, 'Age'] = (data.loc[0, 'Age'] - 18)/(50-18)

        #encoding binary values(yes/no)-------------
        encodeYesNo(data, 'family_history')
        encodeYesNo(data, 'obs_consequence')

        #encoding work interfer---------------------
        work_interfere = {'Never' : 1,
                        'Rarely' : 2, 
                        'Sometimes' : 3, 
                        'Often' : 4
                        }

        data['work_interfere_odinary'] = data.work_interfere.map(work_interfere)
        data.drop(['work_interfere'], axis = 1, inplace = True)

        #encoding benefits------------------------------
        benefits = {'Yes' : 1,
                    'NA' : 0.5, 
                    'No' : 0, 
                    }

        data['benefits_ordinal'] = data.benefits.map(benefits)
        data.drop(['benefits'], axis = 1, inplace = True)

        #encoding care options---------------------------
        care = {'Yes' : 1,
                'NA' : 0.5, 
                'No' : 0, 
                }

        data['care_options_ordinal'] = data.care_options.map(care)
        data.drop(['care_options'], axis = 1, inplace = True)

        #encoding anonymity-------------------------------
        anonymity = {'Yes' : 1,
                    'NA' : 0.5, 
                    'No' : 0, 
                    }

        data['anonymity_ordinal'] = data.anonymity.map(anonymity)
        data.drop(['anonymity'], axis = 1, inplace = True)

        #encoding leave-----------------------------------
        leave = {"Very difficult" : 0, 
                "Somewhat difficult" : 1, 
                "Somewhat easy" : 2, 
                "Very easy" : 3, 
                "NA" : 1.5   
                }

        data['leave_ordinal'] = data.leave.map(leave)
        data.drop(['leave'], axis = 1, inplace = True)

        #encoding mental health consequences--------------
        mental = {'Yes' : 1,
                "NA" : 0.5, 
                'No' : 0, 
                }

        data['mental_health_consequence_ordinal'] = data.mental_health_consequence.map(mental)
        data.drop(['mental_health_consequence'], axis = 1, inplace = True)

        #physical health interview-------------------------
        supervisor = {'Yes' : 1,
                    'NA' : 0.5, 
                    'No' : 0, 
                    }

        data['supervisor_ordinal'] = data.supervisor.map(supervisor)
        data.drop(['supervisor'], axis = 1, inplace = True)

        #encoding physical health interview-----------------
        phy = {'Yes' : 1,
                "NA" : -1, 
                'No' : 0, 
                }

        data['phys_health_interview_ordinal'] = data.phys_health_interview.map(phy)
        data.drop(['phys_health_interview'], axis = 1, inplace = True)

        #encoding number of employees-----------------------
        no_emp = { "1-5" :0, 
                "6-25":1, 
                "26-100":2, 
                "100-500":3, 
                "500-1000":4, 
                "More than 1000":5   
                }

        data['no_employees_ordinal'] = data.no_employees.map(no_emp)
        data.drop(['no_employees'], axis = 1, inplace = True)

        #Encoding Gender
        if(data.loc[0, 'Gender'] == 'male'):
            data['male'] = 1
            data['female'] = 0

        elif(data[0, 'Gender'] == 'female'):
            data['male'] = 0
            data['female'] = 1

        else:
            data['male'] = 0
            data['female'] = 0

        data.drop(['Gender'], axis = 1, inplace = True)
        data.insert(loc = 0, column = 'x0', value = 1)
        
        return True, data
        
    except Exception as e:
        return False, e
        

#home route
@app.route('/')
def home():
    return render_template('api.html')

#prediction system
@app.route('/predict', methods = ['POST'])
def predict():
    
    data = request.get_json(force=True)
    df = pd.DataFrame([json.loads(data)])
    flag, X = process_data(df)
    if flag:
        predict = model.predict(X)
        prob = model.predict_proba(X)
        predict_prob = [prob[0][0], prob[0][1]]
        output = {'flag':1, 'predict' : str(predict[0]), 'prob': predict_prob}
        return json.dumps(output)
    else:
        output = {'flag':0, 'error' : '{} error'.format(X)}
        return json.dumps(output)
