import requests

url = 'http://localhost:5000/predict'
data = requests.post(url,json = {"family_history": "Yes", "care_options": "No", "work_interfere": "Sometimes", "Gender": "male", "benefits": "Don\'t know", "obs_consequence": "No", "no_employees": "6-25", "mental_health_consequence": "Maybe", "supervisor": "Yes", "phys_health_interview": "Maybe", "Age": "42", "leave": "Don\'t know", "anonymity": "Don\'t know"})


print(data.text)
