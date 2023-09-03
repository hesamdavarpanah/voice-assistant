from redis import Redis


class InsertData:
    def __init__(self, pool, data, name):
        self.pool = pool
        self.data = data
        self.name = name
        self.rd = Redis(connection_pool=self.pool, decode_responses=True, charset="utf-8")

    def insert(self):
        try:
            for key, value in self.data.items():
                self.rd.hsetnx(self.name, key, str(value))
        except Exception as e:
            print(f"\33[31m error: {e}")
            return {"error": e}
