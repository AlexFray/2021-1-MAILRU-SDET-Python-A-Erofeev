import re


def count_requests(builder, path):
    count = 0
    with open(path) as file:
        while file.readline():
            count += 1

    builder.create_count_requests(count)


def count_requests_type(builder, path):
    with open(path) as file:
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

        for key, value in count.items():
            builder.create_count_req_type(key, value)


def count_top_resource(builder, path, count_data):
    with open(path) as file:
        count = {}
        line = file.readline()
        while line:
            attr = line.split(' ')
            count[f'{attr[6]}'] = count[f'{attr[6]}'] + 1 if count.get(f'{attr[6]}') else 1
            line = file.readline()
        list_count = list(count.items())
        list_count.sort(key=lambda i: i[1])

    for line in list_count[len(list_count) - count_data:]:
        builder.create_count_top_res(line[0], line[1])


def big_requests_error(builder, path, count_data):
    results = set()
    with open(path) as file:
        line = file.readline()
        while line:
            attr = line.split(' ')
            if re.search(r'4\d{2}', attr[8]):
                results.add((attr[6], attr[8], int(attr[9]), attr[0]))
            line = file.readline()
        results = list(results)
        results.sort(key=lambda i: i[2])

    for line in results[len(results) - count_data:]:
        builder.create_big_req_error(line[0], line[1], line[2], line[3])


def internal_error(builder, path, count_data):
    with open(path) as file:
        result = {}
        line = file.readline()
        while line:
            attr = line.split(' ')
            if re.search(r'5\d{2}', attr[8]):
                result[f'{attr[0]}'] = result[f'{attr[0]}'] + 1 if result.get(f'{attr[0]}') else 1
            line = file.readline()
        list_count = list(result.items())
        list_count.sort(key=lambda i: i[1])

    for line in list_count[len(list_count) - count_data:]:
        builder.create_internal_error(line[0], line[1])
