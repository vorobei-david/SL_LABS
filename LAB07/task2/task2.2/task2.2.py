import json 

with open('11.json', 'r') as file:
    data_all = json.load(file)
result = data_all
data = data_all['translators']

def find_translators_by_language(translators, lang):
    return [t for t in translators if t['language'] == lang]

average_special = {}

def calculate_avg_rate_by_specialization(special):
    for spec in special:
        average_special[spec['specialization']] = spec['rate']

average_experience = {}

def calculate_avg_experience_by_language(experience):
    for exp in experience:
        average_experience[exp['language']] = exp['experience_years']

calculate_avg_rate_by_specialization(data)
calculate_avg_experience_by_language(data)

result = {'average_by_special' : average_special, 'average_exp' : average_experience}


with open('out.json', 'w') as file:
    json.dump(result, file, ensure_ascii=False, indent=4)


