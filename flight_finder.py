import requests
import flight_data


class FlightFinder:
    """
    Class responsible for communication with Fling Finder Api.
    """

    def __init__(self, api_end: str, api_key: str) -> None:
        """
        Initialise data attributes for FlightFinder class
        :param api_end: Api endpoint.
        :param api_key: Api key.
        """
        self.api_end = api_end
        self.header = {
            'apikey': api_key
        }

    def find_data(self, query: str) -> dict:
        """
        Return data from api based on `query`.
        :param query: String to serch api by.
        """
        api_endpoint = f"{self.api_end}locations/query"
        params = {
            'term': query
        }
        response = requests.get(url=api_endpoint,
                                headers=self.header,
                                params=params)
        response.raise_for_status()
        return response.json()

    def find_cheap_flights(self, flight_from: str,
                           flight_to: str, date_from: str,
                           date_to: str,
                           price_to: int, ):
        """
        :param flight_from: Departure IATA city code.
        :param flight_to: Destination IATA city code.
        :param date_from: Search flights from this date. Format
            dd/mm/yyyy.
        :param date_to: Search flights to this date. Format
            dd/mm/yyyy.
        :param price_to: Maximal price of the tickets in GBP.
        """

        api_endpoint = f"{self.api_end}v2/search"
        flight_query = {
            'fly_from': flight_from,
            'fly_to': flight_to,
            'date_from': date_from,
            'date_to': date_to,
            'nights_in_dst_from': 7,
            'nights_in_dst_to': 28,
            'curr': 'GBP',
            'price_to': price_to,
            'sort': 'price',
            'limit': 1,
            'one_for_city': 1,
            'max_stopovers': 0
        }
        response = requests.get(url=api_endpoint, headers=self.header,
                                params=flight_query)
        response.raise_for_status()
        data = response.json()
        try:
            origin_city = data['data'][0]['route'][0]['cityFrom']
        except IndexError:
            return None
        else:
            flight_details = flight_data.FlightData(
                city_from=origin_city,
                airport_from=data['data'][0]['route'][0]['flyFrom'],
                city_to=data['data'][0]['route'][0]["cityTo"],
                airport_to=data['data'][0]['route'][0]["flyTo"],
                time_from= \
                    data['data'][0]['route'][0]["local_departure"].split("T")[0],
                time_to= \
                    data['data'][0]['route'][1]["local_departure"].split("T")[0],
                price=data['data'][0]["price"]
            )
            return flight_details
