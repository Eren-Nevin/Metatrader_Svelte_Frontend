import json as standard_json

import hashlib
import threading
import time
import schedule


from pprint import pprint
import dataclasses
from pathlib import Path
from dataclasses import dataclass
from sanic import Sanic, Request, file, json, response, text
from sanic_ext import Extend
from sanic_httpauth import HTTPBasicAuth


from models import AppState

from xe_crawler import XeResult, XeCrawler
from utilities import read_config_file


from dataclass_wizard import fromdict, asdict
server_address = '0.0.0.0'
server_port = 7777


auth = HTTPBasicAuth()

app_salt = "APP_SECRET"


def hash_password(salt, password):
    salted = password + salt
    return hashlib.sha512(salted.encode("utf8")).hexdigest()


config = read_config_file(Path('./secrets.yml'))

default_users = {
}

for user, password in config['auth'].items():
    default_users[user] = hash_password(app_salt, password)


# users = {
#     "john": hash_password(app_salt, "hello"),
#     "susan": hash_password(app_salt, "bye"),
# }


@auth.verify_password
def verify_password(username, password):
    if username in default_users:
        return default_users.get(username) == hash_password(app_salt, password)
    return False


def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


class Server:
    def __init__(self) -> None:
        self.app = Sanic("My_Server")
        self.app.config.LOCAL_CERT_CREATOR = 'trustme'
        self.app.config['CORS_SUPPORTS_CREDENTIALS'] = True
        self.app.config.CORS_ORIGINS = "http://lord-bot.com"
        Extend(self.app)

        self.xe_crawler = XeCrawler()
        # xe_rates: XeResult = self.xe_crawler.get_xe_rates(True)

        self.app_state = AppState.initialize_test()

        load_res = self.load_state_from_file(Path('./app_state.json'))
        if load_res:
            print("Successuflly loaded app state", flush=True)

        self.last_rates = self.update_app_state_with_xe(True)
        # self.last_rates = self.xe_crawler.get_xe_rates(True)

        # self.app_state.currency_model.currency_rates =\
        #     self.xe_crawler.convert_xe_results_to_currency_rate_list(xe_rates)

        # self.app.add_route(self.get_all_rates, 'api/get_all_rates', ['GET'])
        self.app.add_route(self.get_state, 'api/get_state', ['GET'])
        self.app.add_route(self.send_state, 'api/send_state', ['POST'])
        self.app.add_route(self.get_saved_state_file,
                           'api/get_state_file', ['GET'])
        self.app.add_route(self.load_app_state_from_file, 'api/send_state_file',
                           ['POST'])
        self.set_serve_static()
        self.app.add_route(auth.login_required(
            self.index), 'index.html', ['GET'])

    def save_state_to_file(self, path: Path):
        def serialize_sets(obj):
            if isinstance(obj, set):
                return list(obj)

            return obj
        print("Saving app_state", flush=True)
        try:
            standard_json.dump(asdict(self.app_state), open(path, 'w'))
            return True
        except Exception as e:
            print(e, flush=True)
        return False

    def load_state_from_file(self, path: Path):
        print("Loading app_state", flush=True)
        try:
            bot_state_raw = standard_json.load(open(path, 'r'))
            self.app_state = fromdict(AppState, bot_state_raw)
            print(f'loaded app state {self.app_state}', flush=True)
            return True
        except Exception as e:
            print(e, flush=True)

        return False

    async def index(self, request: Request):
        path = Path('../public')
        html_path = path.resolve().joinpath('./index.html')
        return response.html(html_path.read_text())

    def set_serve_static(self):
        path = Path('../public')
        self.app.static('/', path.resolve())
        # html_path = path.resolve().joinpath('/index.html')
        # self.app.static('/index.html', html_path, name='index')

    # async def get_all_rates(self, request: Request):

    #     if self.last_rates:
    #         res = json({'status': 'ok', 'message': {'timestamp': self.last_rates.timestamp,
    #                     'rates': self.last_rates.rates
    #                                                 }}, )
    #         res.headers.extend({'Access-Control-Allow-Origin': '*'})
    #         return res
    #     else:
    #         res = json({'status': 'fail', 'message': 'Last rates is empty'})
    #         return res

    async def get_saved_state_file(self, request: Request):
        print("Sending saved state file")
        res = await file('./app_state.json')
        return res

    async def load_app_state_from_file(self, request: Request):
        print(request.url)
        print(request.files)
        if req_files := request.files:
            state_file = req_files.get('file')
            static_file_content_binary = state_file.body
            with open(Path('./app_state.json'), 'wb') as file:
                file.write(static_file_content_binary)
                print("WROTE")
                self.load_state_from_file(Path('./app_state.json'))
        return text("OK")

    async def get_state(self, request: Request):
        print("Updating rates", flush=True)
        # self.update_app_state_with_xe()
        print("Sending State to client", flush=True)
        res = json(dataclasses.asdict(self.app_state))
        res.headers.extend({'Access-Control-Allow-Origin': '*'})

        return res

    async def send_state(self, request: Request):
        print("Getting state from client", flush=True)
        self.app_state = fromdict(AppState, request.json)

        pprint(asdict(self.app_state))
        save_res = self.save_state_to_file(Path('./app_state.json'))
        if save_res:
            print('Successfully saved state to file', flush=True)

        return json({'status': 'OK'})

    def update_app_state_with_xe_result(self, xe_result: XeResult):
        for currency_rate in self.app_state.currency_model.currency_rates:
            if currency_rate.currencyCode in xe_result.rates:
                currency_rate.rate =\
                    round(xe_result.rates[currency_rate.currencyCode],
                          4)

    def update_app_state_with_xe(self, refresh_auth=True):
        if last_xe_rates := self.xe_crawler.get_xe_rates(refresh_auth):
            self.update_app_state_with_xe_result(last_xe_rates)
            return last_xe_rates
        else:
            return None

    # This checks the xe website each minute and updates the app state.

    def start_continous_xe_crawling(self):
        schedule.every(1).minutes.do(self.update_app_state_with_xe)
        stop_run = run_continuously()
        return stop_run


server = Server()

if __name__ == '__main__':
    stop_run = server.start_continous_xe_crawling()
    server.app.run(server_address, server_port)
    # stop_run.set()
