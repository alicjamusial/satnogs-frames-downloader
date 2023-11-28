import requests
import os
import json
from datetime import datetime


def create_dir():
    path = "./data/"
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory {} failed. Please create it by yourself and run script again".format(
                path), flush=True)
            exit()
        else:
            print("Successfully created the directory {} ".format(path), flush=True)
    return path


class TelemetryDownloader:
    def __init__(self, args):
        self.token = 'Token {}'.format(args.accessToken)
        self.satellite = args.satelliteId

        self.start = args.startDate
        self.end = args.endDate

        self.numberOfPages = args.numberOfPages
        self.validLength = args.validLength

        self.url = "https://db.satnogs.org/api/telemetry/?satellite=" + self.satellite

        self.telemetry = []

    def fetch_telemetry(self):
        filters = ''
        filters += "&start=" + self.start if self.start else ''
        filters += "&end=" + self.end if self.end else ''
        filters += "&results=d1"

        page = 1

        while True:
            url = self.url + "&page=" + str(page) + filters
            response = requests.get(url, headers={'Authorization': self.token})

            if response.status_code == 401:
                print("The token is invalid. Try again.", flush=True)
                exit()

            elif response.status_code == 200:
                current_data = json.loads(response.text)

                if type(current_data) is list:
                    self.telemetry = self.telemetry + current_data
                    print('Page {} loaded. {} frames fetched.'.format(page, len(current_data)), flush=True)
                else:
                    print('There were no proper frames found. Received data: {}'.format(current_data), flush=True)

            elif response.status_code == 404:  # no more pages
                print('All pages loaded.')
                break

            else:
                print('There is something wrong with the response. Status code: {}'.format(response.status_code),
                      flush=True)

                exit()

            page += 1
            if self.numberOfPages is not None and page > self.numberOfPages:
                print('All requested pages ({}) loaded.'.format(self.numberOfPages))
                break

        print('\nAll frames count: {}\n'.format(str(len(self.telemetry))), flush=True)

    def reverse_telemetry(self):
        self.telemetry = self.telemetry[::-1]

    def filter_telemetry(self):
        self.telemetry = list(
            filter(
                lambda single: len(single['frame']) == self.validLength,
                self.telemetry))

    def print_info(self):
        if len(self.telemetry) > 0:
            print('First valid frame timestamp: {}'.format(self.telemetry[0]['timestamp']),
                  flush=True)
            print('Last valid frame timestamp: {}'.format(self.telemetry[len(self.telemetry) - 1]['timestamp']),
                  flush=True)

    def create_file_hex(self):
        writeable_telemetry = ''
        for single_frame in self.telemetry:
            writeable_telemetry += single_frame['frame']
        path = create_dir()

        file_name = path + str(datetime.today().strftime('%Y-%m-%d-%H-%M-%S')) + "-telemetry.hex"
        file = open(file_name, "wb")
        file.write(bytearray.fromhex(writeable_telemetry))
        file.close()
        print('\nAll frames saved to file: {}\n'.format(file_name), flush=True)

    def create_file_json(self):
        writeable_telemetry = json.dumps(self.telemetry)
        path = create_dir()

        file_name = path + str(datetime.today().strftime('%Y-%m-%d-%H-%M-%S')) + "-telemetry.json"
        file = open(file_name, "w")
        file.write(writeable_telemetry)
        file.close()
        print('\nAll frames saved to file: {}\n'.format(file_name), flush=True)

