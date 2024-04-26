import request

base_url = 'https://api.lufthansa.com/v1/offers/faresbestprice/'


def get_lowest_fares(origin, 
                     destination, 
                     travel_date,
                     return_date,
                     cabin_class, 
                     travelers,
                     country):
    """
    getting lowest fares
    :param origin:
    :param destination:
    :param travel_date:	
    :param return_date:
    :param cabin_class:
    :param travelers:  (adult=1)
    :param country:
    :return schedule json object:
    """
    url = base_url+'lowestfares/'+origin+'/'+destination+'/'+travel_date+'/'+return_date+'/'+cabin_class+'/'+travelers+'/'+country
    return request.make_request(url)