from redis import ConnectionPool, exceptions


class RedisConfiguration:
    def __init__(self, host, port, db_number):
        self.host = host
        self.port = port
        self.db_number = db_number

    @property
    def connection_pool(self):
        try:
            pool = ConnectionPool(host=self.host, port=self.port, db=self.db_number)
            return pool
        except exceptions.AuthenticationError:
            print(f"\33[31merror: {exceptions.AuthenticationError}")
            return {"error": "invalid_password"}
        except exceptions.ConnectionError:
            print(f"\33[31merror: {exceptions.ConnectionError}")
            return {"error": "invalid_host_or_port"}
        except Exception as e:
            print(f"\33[31merror: {e}")
            return {"error": f"{e}"}
