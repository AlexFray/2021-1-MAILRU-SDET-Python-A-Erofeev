import argparse
import json
import re

parser = argparse.ArgumentParser(description='Для сохранения файла в json ')
parser.add_argument('--json', action='store_true')
args = parser.parse_args()

with open('access.log') as file:
    result = {}
    line = file.readline()
    while line:
        attr = line.split(' ')
        if re.search(r'5\d{2}', attr[8]):
            result[f'{attr[0]}'] = result[f'{attr[0]}'] + 1 if result.get(f'{attr[0]}') else 1
        line = file.readline()
    list_count = list(result.items())
    list_count.sort(key=lambda i: i[1])

filename = f'internal_errors.{"json" if args.json else "txt"}'
with open(filename, 'w') as file:
    if args.json:
        result = []
        for res in list_count[len(list_count) - 5:]:
            result.append(
                {
                    'ip': res[0],
                    'count': res[1]
                }
            )
        json.dump({"result": result}, file)
    else:
        results = list_count[len(list_count) - 5:]
        file.write('ip | count \n')
        for line in results:
            file.write(f'{line[0]} | {line[1]}\n')
