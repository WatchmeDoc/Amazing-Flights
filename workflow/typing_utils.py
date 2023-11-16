from typing import List, TypedDict


class DateDict(TypedDict):
    year: int  # required
    month: int
    day: int


class RequestDict(TypedDict):
    originLocationCode: str  # required
    destinationLocationCode: str  # required
    departureDate: str  # required
    adults: int  # required
    children: int
    infants: int
    travelClass: str
    includedAirlineCodes: List[str]
    excludedAirlineCodes: List[str]
    nonStop: bool
    currencyCode: str


class FlightDict(TypedDict):
    at: str  # date yyyy-mm-ddThh:mm:ss format
    iataCode: str  # airport code


class SegmentDict(TypedDict):
    aircraft: dict  # aircraft information
    arrival: FlightDict  # arrival information
    blacklistedInEU: bool
    carrierCode: str
    departure: FlightDict  # departure information
    duration: str  # duration of the segment format `PTXHYM` (e.g. PT2H30M)
    id: int
    number: int
    numberOfStops: int
    operating: dict  # operating information


class ItineraryDict(TypedDict):
    duration: str  # duration of the segment format `PTXHYM` (e.g. PT2H30M)
    segments: List[SegmentDict]


class PriceDict(TypedDict):
    additionalServices: List[dict]
    base: float
    currecny: str
    fees: List[dict]
    grandTotal: float
    total: float


class ResponseDataDict(TypedDict):
    id: int  # result number
    instantTicketingRequired: bool
    itineraries: List[ItineraryDict]
    lastTicketingDate: str  # date yyyy-mm-dd format
    lastTicketingDateTime: str  # date yyyy-mm-dd format
    oneWay: bool
    price: PriceDict
    pricingOptions: dict
    travelerPricings: List[dict]
    type: str
    validatingAirlineCodes: List[str]


# This is kept only for information purposes. It is not used in the code.
# class ResponseDict(TypedDict):
#     body: dict  # metadata, number of flights, links, etc.
#     data: List[ResponseDataDict]  # list of flights
#     headers: HTTPMessage
#     http_response: HTTPResponse
#     parsed: bool  # whether the response was parsed successfully
#     request: Request
#     result: dict  # the actual result of the query
#     status_code: int
