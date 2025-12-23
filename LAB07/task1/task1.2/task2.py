with open('input.txt', 'r') as file:
    for line in file:
        with open('output.txt', 'a') as file2:
            res = line.lower()
            file2.write(res)