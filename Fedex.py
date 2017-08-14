#Help taken from the bbelow link
#https://stackoverflow.com/questions/18817185/parsing-html-does-not-output-desired-datatracking-info-for-fedex

import requests
import json

tracking_number = '744668909687'

data = requests.post('https://www.fedex.com/trackingCal/track', data={
    'data': json.dumps({
        'TrackPackagesRequest': {
            'appType': 'wtrk',
            'uniqueKey': '',
            'processingParameters': {
                'anonymousTransaction': True,
                'clientId': 'WTRK',
                'returnDetailedErrors': True,
                'returnLocalizedDateTime': False
            },
            'trackingInfoList': [{
                'trackNumberInfo': {
                    'trackingNumber': tracking_number,
                    'trackingQualifier': '',
                    'trackingCarrier': ''
                }
            }]
        }
    }),
    'action': 'trackpackages',
    'locale': 'en_US',
    'format': 'json',
    'version': 99
}).json()

tracking_number_key = 'trackingNbr'
ship_time_key = 'displayShipDt'
status_key = 'status'
ship_arrival_key = 'displayActDeliveryDateTime'
output = {}
for key, value in data.items():
    narrow = value
    #narrow more into packageList list
    for key, value in narrow.items():
        if key == 'packageList':
            narrow = value
    for x, y in narrow[0].items():
        if x == tracking_number_key:
            output['tracking no'] = y
        elif x == ship_time_key:
            output['ship date'] = y
        elif x == status_key:
            output['status'] = y
        elif x == ship_arrival_key:
            output['scheduled delivery'] = y

print(output)