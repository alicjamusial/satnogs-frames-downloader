import argparse
from downloader import TelemetryDownloader


def main(args):
    downloader_telemetry = TelemetryDownloader(args)

    downloader_telemetry.fetch_telemetry()
    downloader_telemetry.prepare_file()
    downloader_telemetry.print_info()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--accessToken', '-t', help='SatNOGS access token', required=True)
    parser.add_argument('--satelliteId', '-i', help='Satellite Norad ID', required=True)
    parser.add_argument('--validLength', '-l', help='Satellite valid frame length (discard any other length frames)')
    parser.add_argument('--startDate', '-s', help='Start date for observations (format: %%Y-%%m-%%dT%%H:%%M:%%SZ)')
    parser.add_argument('--endDate', '-e', help='End date for observations (format: %%Y-%%m-%%dT%%H:%%M:%%SZ)')
    parser.add_argument('--outputMerge', '-m', help='Merge telemetry files into one .hex (default: false)',
                        action='store_true',
                        default=False)
    parser.add_argument('--outputReverse', '-r', action='store_true',
                        help='Reverse telemetry order in merged file - works only with merge (default: false)',
                        default=False)
    return parser.parse_args()


main(parse_args())
