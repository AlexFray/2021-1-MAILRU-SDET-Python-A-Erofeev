import argparse
import json

parser = argparse.ArgumentParser(description='Для сохранения файла в json ')
parser.add_argument('--json', action='store_true')
args = parser.parse_args()

with open('access.log') as file:
    count = {}
    line = file.readline()
    while line:
        attr = line.split(' ')
        count[f'{attr[6]}'] = count[f'{attr[6]}'] + 1 if count.get(f'{attr[6]}') else 1
        line = file.readline()
    list_count = list(count.items())
    list_count.sort(key=lambda i: i[1])

filename = f'count_top_resource.{"json" if args.json else "txt"}'
with open(filename, 'w') as file:
    if args.json:
        result = []
        for res in list_count[len(list_count) - 10:]:
            result.append(
                {
                    'path': res[0],
                    'count': res[1]
                }
            )
        json.dump({"result": result}, file)
    else:
        results = list_count[len(list_count) - 10:]
        file.write('url | count \n')
        for line in results:
            file.write(f'{line[0]} | {line[1]}\n')
