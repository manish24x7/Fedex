import requests
import json

daysdict = {1:31,2:28,3:31,4:31,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
def days_in_month(month):
    for key, value in daysdict.iteritems():
        if key == month:
            number_of_days = value
    return number_of_days

tracking_number = '744668909687'


def build_output(tracking_number):

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

    return data

# finds delivery date info

ship_arrival_key = 'displayActDeliveryDateTime'
ship_time_key = 'displayShipDt'



def track(tracking_number):

    data = build_output(tracking_number)
     #narrowing down dictionary and lists to objects needed (ship day,arrival)
    for key, value in data.iteritems():
        narrow = value 
    #narrow more into packageList list
    for key, value in narrow.iteritems():
        if key == 'packageList':
            narrow = value
    # narrow to ship start value
    for x, y in narrow[0].iteritems():
        if x == ship_arrival_key:
            ship_arival_value = y
            exists = True

    # also find ship arrival
        elif x == ship_time_key:
            ship_time_value = y
            exists = True
    # list with two items shiptime and shiparrival

    return  ship_time_value, ship_arival_value, exists


def print_results(tracking_number):
    to_fro = track(tracking_number)
    if to_fro[2] == True:
        try:
            daysinmonth = days_in_month(int(to_fro[0][0]))
            try:
                if to_fro[0][0] != to_fro[1][0]:

                    ship_days = str(    (int(daysinmonth) - int(str((to_fro[0][2]))+str((to_fro[0][3])))  + int(to_fro[1][3])) )

                    print '_____________________'
                    print 'Shipped: ' + to_fro[0]
                    print 'Arrived: ' + to_fro[1]
                    print '_____________________'
                    print '\nShipping took:' +"     "  +ship_days  
                else:
                    ship_days = int(to_fro[1][2] + to_fro[1][3]) - int(to_fro[0][2] + to_fro[0][3])
                    print '_____________________'
                    print 'Shipped: ' + to_fro[0]
                    print 'Arrived: ' + to_fro[1]
                    print '_____________________'
                    print  '\nShipping took:' +"    " +  str(ship_days)  
            except IndexError:
                print 'Invalid Tracking Number'
                pass
        except IndexError:
            pass
    else:
        pass

def raw_results(tracking_number):
    to_fro = track(tracking_number)
    if to_fro[2] == True:
        daysinmonth = days_in_month(int(track(tracking_number)[0][0]))
        try:
            if to_fro[0][0] != to_fro[1][0]:

                ship_days = str(    (int(daysinmonth) - int(str((to_fro[0][2]))+str((to_fro[0][3])))  + int(to_fro[1][3])) )
            else:
                ship_days = int(to_fro[1][2] + to_fro[1][3]) - int(to_fro[0][2] + to_fro[0][3])
        except IndexError:
            print 'Invalid Tracking Number'
            pass
    else:
        pass

    return ship_days



#print_results(499552080632881)