import csv
import os

def dict2csv(dict):

    if not os.path.exists('output'):
        os.makedirs('output')

    with open('output/' + dict['name'] + '.csv', 'w') as file:
        writer = csv.DictWriter(file, dict.keys())
        writer.writeheader()
        writer.writerow(dict)

if __name__ == '__main__':
    dict2csv({"name": "1", "testing": "2"})