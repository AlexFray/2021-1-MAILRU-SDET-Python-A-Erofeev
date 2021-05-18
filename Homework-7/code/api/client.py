import json
import logging
import socket


logger = logging.getLogger('test')


class ErrorRequest(Exception):
    pass


class ClientSocket:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def connection(self, method, path, data=None):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((self.host, self.port))
            request = self.request(method, path, data)
            s.sendall(request)
            total_data = []
            while True:
                data = s.recv(4096)
                if data:
                    total_data.append(data.decode())
                else:
                    break
            data = ''.join(total_data).splitlines()
            code = int(data[0].split(' ')[1])
            response = data[-1]
            logger.info(f"Response: code = {code}, data = {response}")
            return code, response

    @property
    def request_headers(self):
        return "{method} {path} HTTP/1.1\r\nContent-Type: application/json\r\nHost: {host}\r\nContent-Length: {content_length}\r\n\r\n"

    def request(self, method, path, data=None):
        content_length = 0
        data_bytes = b''
        if data:
            data = str(data)
            content_length = len(data)
            data_bytes += data.encode('iso-8859-1')
        headers = self.request_headers.format(method=method, path=path, host=self.host, content_length=content_length)
        headers_bytes = headers.encode('iso-8859-1')
        logger.info(headers.replace('\r\n', ' ') + (data if data else ""))
        return headers_bytes + data_bytes

    def get_user(self, id, extended_code=200):
        code, response = self.connection('GET', f'/user/{id}')
        if code != extended_code:
            raise ErrorRequest(f'Ошибка получения пользователя. {code} != {extended_code}, ответ: {response}.')
        return json.loads(response)

    def post_user(self, name_user, extended_code=201):
        data = {"name": name_user}
        code, response = self.connection('POST', '/user', data)
        if code != extended_code:
            raise ErrorRequest(f'Ошибка создание пользователя. {code} != {extended_code}, ответ: {response}.')
        return json.loads(response)

    def put_user(self, id, new_name, extended_code=200):
        data = {"name": new_name}
        code, response = self.connection('PUT', f'/user/{id}', data)
        if code != extended_code:
            raise ErrorRequest(f'Ошибка обновления пользователя. {code} != {extended_code}, ответ: {response}.')
        return json.loads(response)

    def delete_user(self, id, extended_code=200):
        code, response = self.connection('DELETE', f'/user/{id}')
        if code != extended_code:
            raise ErrorRequest(f'Ошибка удаления пользователя. {code} != {extended_code}, ответ: {response}.')
        return json.loads(response)
