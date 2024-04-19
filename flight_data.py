class FlightData:
    """
    Representation of the class containing information about the flight.
    """

    def __init__(self, city_from: str, airport_from: str, city_to: str,
                 airport_to: str, time_from: str, time_to: str,
                 price: int):
        """
        Initialize data attributes.
        :param city_from: City of the departure.
        :param airport_from: Departure airport.
        :param city_to: Destination city.
        :param airport_to: Destination airport.
        :param time_from: Beginning of trip.
        :param time_to: End of the trip.
        :param price: Price for the trip.
        """
        self.city_from = city_from
        self.airport_from = airport_from
        self.city_to = city_to
        self.airport_to = airport_to
        self.time_from = time_from
        self.time_to = time_to
        self.price = price
