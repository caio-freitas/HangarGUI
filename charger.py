import httplib2

RANGE = 5 # 5 V


class Charger():
    def __init__(self):
        self.enabled = False
        self.level = -1
        self.voltage = -1
        self.client =

    def enable_charge(self, boolean):
        if boolean:
            logging.warning("Charging enabled")
            PATH = 'charge_enable'
            data = 'charge_enable'
            url = "http://" + self.esp_ip + '/' + PATH
            try:
                response, content = self.http.request(url, "PUT", body=data)
            except Exception as e:
                print(e)
                pass
        else:
            logging.warning("Charging enabled")
            PATH = 'charge_disable'
            data = 'charge_disable'
            url = "http://" + self.esp_ip + '/' + PATH
            try:
                response, content = self.http.request(url, "PUT", body=data)
            except Exception as e:
                print(e)
                pass
        self.enable = True

    def update_params(self):
        wifi client
        self.voltage = level*RANGE



def test():
    charger = Charger()


if __name__ == "__main__":
    test()
