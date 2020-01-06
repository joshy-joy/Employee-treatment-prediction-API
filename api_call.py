import requests

url = 'http://127.0.0.1:5002/predict'
data = {"family_history": "Yes", 
                                  "care_options": "No", 
                                  "work_interfere": "Sometimes", 
                                   "Gender": "male", 
                                    "benefits": "na", 
                                    "obs_consequence": "No", 
                                    "no_employees": "6-25", 
                                    "mental_health_consequence": "Maybe", 
                                    "supervisor": "Yes", 
                                    "phys_health_interview": "Maybe", 
                                    "Age": "42",
                                    "anonymity": "na", 
                                    "leave": "na", 
                        
                                    }
data = requests.post(url,json = {'data': data })


print(data.text)
