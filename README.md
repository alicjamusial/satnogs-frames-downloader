## SatNOGS frames downloader 📡

Python script to automatically download SatNOGS data from a chosen satellite and create `.hex` or `.json` file with the results.

#### Requirements
- python > 3.5.0
- [access token](https://community.libre.space/t/satnogs-db-telemetry-api-endpoint/5341) for SatNOGS DB

#### Usage
```
python run.py [-h] --accessToken ACCESSTOKEN --satelliteId SATELLITEID --output {json,hex} [--validLength VALIDLENGTH] [--startDate STARTDATE] [--endDate ENDDATE] [--numberOfPages NUMBEROFPAGES] [--reverseTelemetry REVERSETELEMETRY]
      
    arguments:
    -h, --help            show this help message and exit
    --accessToken ACCESSTOKEN, -t ACCESSTOKEN
                        SatNOGS access token
    --satelliteId SATELLITEID, -i SATELLITEID
                        Satellite Norad ID
    --output {json,hex}, -o {json,hex}
                        Output as a json or hex file
    --validLength VALIDLENGTH, -l VALIDLENGTH
                        Satellite valid frame length (discard any other length frames)
    --startDate STARTDATE, -s STARTDATE
                        Start date for observations (format: %Y-%m-%dT%H:%M:%SZ)
    --endDate ENDDATE, -e ENDDATE
                        End date for observations (format: %Y-%m-%dT%H:%M:%SZ)
    --numberOfPages NUMBEROFPAGES, -n NUMBEROFPAGES
                        Maximum number of pages to download
    --reverseTelemetry REVERSETELEMETRY, -r REVERSETELEMETRY
                        Reverse telemetry frames order (default: false)
```

Example usage: `python run.py --accessToken ##################################### --satelliteId 44426 --numberOfPages 2 --output json`
