from http.client import HTTPMessage, HTTPResponse
from typing import List, TypedDict

from amadeus.client.request import Request


class DateDict(TypedDict):
    year: int
    month: int
    day: int


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


class DataDict(TypedDict):
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


class QueryResponse(TypedDict):
    body: dict  # metadata, number of flights, links, etc.
    data: List[DataDict]  # list of flights
    headers: HTTPMessage
    http_response: HTTPResponse
    parsed: bool  # whether the response was parsed successfully
    request: Request
    result: dict  # the actual result of the query
    status_code: int
