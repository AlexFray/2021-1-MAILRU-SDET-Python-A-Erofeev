from mysql.models import *


class MySQLBuilder:

    def __init__(self, client):
        self.client = client

    def create_count_requests(self, count):
        cr = CountRequests(count=count)
        self.client.session.add(cr)
        return cr

    def create_count_req_type(self, type, count):
        crt = CountRequestsType(
            type=type,
            count=count
        )
        self.client.session.add(crt)
        return crt

    def create_count_top_res(self, path, count):
        ctr = CountTopResources(
            path=path,
            count=count
        )
        self.client.session.add(ctr)
        return ctr

    def create_internal_error(self, ip, count):
        ie = InternalErrors(ip=ip, count=count)
        self.client.session.add(ie)
        return ie

    def create_big_req_error(self, path, code, size, ip):
        bre = BigRequestsError(
            path=path,
            code=code,
            size=size,
            ip=ip
        )
        self.client.session.add(bre)
        return bre
