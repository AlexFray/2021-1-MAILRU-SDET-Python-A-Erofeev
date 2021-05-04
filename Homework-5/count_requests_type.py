import argparse
import json

parser = argparse.ArgumentParser(description='Для сохранения файла в json ')
parser.add_argument('--json', action='store_true')
args = parser.parse_args()

with open('access.log') as file:
    line = file.readline()
    count = {}
    while line:
        if ' "POST ' in line:
            count['POST'] = count['POST'] + 1 if count.get('POST') else 1
        elif ' "GET ' in line:
            count['GET'] = count['GET'] + 1 if count.get('GET') else 1
        elif ' "PUT ' in line:
            count['PUT'] = count['PUT'] + 1 if count.get('PUT') else 1
        elif ' "HEAD ' in line:
            count['HEAD'] = count['HEAD'] + 1 if count.get('HEAD') else 1
        line = file.readline()

filename = f'count_requests_type.{"json" if args.json else "txt"}'
with open(filename, 'w') as file:
    if args.json:
        json.dump(count, file)
    else:
        file.write('POST | GET | PUT | HEAD\n')
        file.write(f'{count["POST"]} | {count["GET"]} | {count["PUT"]} | {count["HEAD"]}')
