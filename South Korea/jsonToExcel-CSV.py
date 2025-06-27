import json
import pandas as pd

# Load data from professors.json
with open('skprofessors.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Add Country field
for prof in data:
    prof['Country'] = 'South Korea'

# Create DataFrame
df = pd.DataFrame(data, columns=['Name', 'Email', 'University', 'Country'])

# Save to CSV
df.to_csv('professors.csv', index=False)

# Save to Excel
df.to_excel('professors.xlsx', index=False)

print("Saved professors.csv and professors.xlsx")