import argparse
import json
import re

parser = argparse.ArgumentParser(description='Для сохранения файла в json ')
parser.add_argument('--json', action='store_true')
args = parser.parse_args()

results = set()
with open('access.log') as file:
    line = file.readline()
    while line:
        attr = line.split(' ')
        if re.search(r'4\d{2}', attr[8]):
            results.add((attr[6], attr[8], int(attr[9]), attr[0]))
        line = file.readline()
    results = list(results)
    results.sort(key=lambda i: i[2])

filename = f'big_requests_error.{"json" if args.json else "txt"}'
with open(filename, 'w') as file:
    if args.json:
        result = []
        for res in results[len(results) - 5:]:
            result.append(
                {
                    'path': res[0],
                    'code': res[1],
                    'size': res[2],
                    'ip': res[3]
                }
            )
        json.dump({"result": result}, file)
    else:
        results = results[len(results) - 5:]
        file.write('path | code | size | ip\n')
        for line in results:
            file.write(f'{line[0]} | {line[1]} | {line[2]} | {line[3]}\n')
