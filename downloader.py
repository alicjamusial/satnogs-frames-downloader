import requests
import json
from datetime import datetime


class TelemetryDownloader:
    def __init__(self, args):
        print(args)
        self.token = 'Token {}'.format(args.accessToken)
        self.satellite = args.satelliteId

        self.start = args.startDate
        self.end = args.endDate

        self.validLength = args.validLength
        self.outputMerge = args.outputMerge
        self.outputReverse = args.outputReverse

        self.url = "https://db.satnogs.org/api/telemetry/?satellite=" + self.satellite

        self.telemetry = []

    def fetch_telemetry(self):
        filters = ''
        filters += "&start=" + self.start if self.start else ''
        filters += "&end=" + self.end if self.end else ''

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

        print('\nAll frames count: ' + str(len(self.telemetry)), flush=True)

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

    def prepare_file(self):
        telemetry_content = ''

        for single in self.telemetry:
            telemetry_content += single['frame'][40:]

        telemetry_content_bytearray = bytearray.fromhex(telemetry_content)

        file_name = str(datetime.today().strftime('%Y-%m-%d-%H-%M-%S')) + "-telemetry.hex"
        file = open(file_name, "wb")
        file.write(telemetry_content_bytearray)
        file.close()

        print('\nAll frames saved to file: {}\n'.format(file_name), flush=True)
