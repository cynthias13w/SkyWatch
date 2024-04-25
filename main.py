import requests
import auth

base_url = 'https://api.lufthansa.com/v1/operations/schedules'

def make_url(url, country, airport, date):
    return f'{url}/{country}/{airport}/{date}'

def make_request(url):
    """
    makes the request to the URL
    :param url:
    :return json object:
    """
    header = auth.get_header()
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        return response.text
    else:
        return 'invalid request'

if __name__ == "__main__":
    # Creating URL
    my_url = make_url(base_url, "FRA", "JFK", "2024-07-15")

    # Requesting info
    response_text = make_request(my_url)
    print(response_text)
