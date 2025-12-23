import csv

data_with = []

with open('10.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        data_with.append(row)
        for key, value in row.items():
            print(f"  {key} -> {value}")


def find_min_max_transaction(data):
    amounts = [int(row['Amount']) for row in data]
    min_am = min(amounts)
    max_am = max(amounts)
    return min_am, max_am

def calculate_total_deposits(data):
    sum = 0
    for row in data:
        if row["Type"] == "Deposit":
            sum += int(row['Amount'])
    return sum

def calculate_avg_transaction_by_account(data):
    average = []
    for row in data:
        if row['Account'] == 'ACC123456':
            average.append(int(row['Amount']))
    if average:
        return sum(average) / len(average)
    
def count_transactions_by_type(data, typeo = 'Deposit'):
    res = 0
    for row in data:
        if row["Type"] == typeo:
            res += 1
    return res

print(find_min_max_transaction(data_with))
print(calculate_total_deposits(data_with))
print(calculate_avg_transaction_by_account(data_with))
print(count_transactions_by_type(data_with))