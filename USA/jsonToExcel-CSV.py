import json
import pandas as pd

with open('usprofessors.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for prof in data:
    prof['Country'] = 'USA'

df = pd.DataFrame(data, columns=['Name', 'Email', 'University', 'Country'])

df.to_csv('professors.csv', index=False)

df.to_excel('professors.xlsx', index=False)

print("Saved professors.csv and professors.xlsx")