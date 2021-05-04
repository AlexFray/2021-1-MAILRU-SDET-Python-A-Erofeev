import argparse
import json

parser = argparse.ArgumentParser(description='Для сохранения файла в json ')
parser.add_argument('--json', action='store_true')
args = parser.parse_args()
count = 0
with open('access.log') as file:
    while file.readline():
        count += 1

filename = f'count_requests.{"json" if args.json else "txt"}'
with open(filename, 'w') as file:
    if args.json:
        json.dump({"requests": count}, file)
    else:
        file.write('Count\n')
        file.write(f'{count}')
