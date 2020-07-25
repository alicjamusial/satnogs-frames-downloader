import argparse
from downloader import TelemetryDownloader


def main(args):
    downloader_telemetry = TelemetryDownloader(args)
    downloader_telemetry.fetch_telemetry()
    if args.validLength:  # filter non-valid frames
        downloader_telemetry.filter_telemetry()
    if args.reverseTelemetry:  # reverse telemetry
        downloader_telemetry.reverse_telemetry()

    if args.output == 'json':
        downloader_telemetry.create_file_json()
    elif args.output == 'hex':
        downloader_telemetry.create_file_hex()

    downloader_telemetry.print_info()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--accessToken', '-t', help='SatNOGS access token', required=True)
    parser.add_argument('--satelliteId', '-i', help='Satellite Norad ID', required=True)
    parser.add_argument('--output', '-o', help='Output as a json or hex file',
                        choices=('json', 'hex'), required=True)
    parser.add_argument('--validLength', '-l', help='Satellite valid frame length (discard any other length frames)')
    parser.add_argument('--startDate', '-s', help='Start date for observations (format: %%Y-%%m-%%dT%%H:%%M:%%SZ)')
    parser.add_argument('--endDate', '-e', help='End date for observations (format: %%Y-%%m-%%dT%%H:%%M:%%SZ)')
    parser.add_argument('--numberOfPages', '-n', help='Maximum number of pages to download', type=int)
    parser.add_argument('--reverseTelemetry', '-r', help='Reverse telemetry frames order (default: false)', type=bool, default=False)
    return parser.parse_args()


main(parse_args())
