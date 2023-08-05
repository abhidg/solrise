"""
Sunrise and sunset calculator
"""

import math
import datetime
from typing import Literal

DEG_TO_RAD = math.pi / 180
zenith = 90.8

sin = lambda degrees: math.sin(DEG_TO_RAD * degrees)
cos = lambda degrees: math.cos(DEG_TO_RAD * degrees)
tan = lambda degrees: math.tan(DEG_TO_RAD * degrees)

asin = lambda val: math.asin(val) / DEG_TO_RAD
acos = lambda val: math.acos(val) / DEG_TO_RAD
atan = lambda val: math.atan(val) / DEG_TO_RAD


class NoSunriseOrSunsetTime(Exception):
    "Raised when no valid sunrise or sunset time is available (sun never sets or rises)"
    pass


def within(val, upper):
    if val < 0:
        return val + upper
    elif val >= upper:
        return val - upper
    else:
        return val


def suntime(
    rise_or_set: Literal["sunrise", "sunset"], latitude, longitude, date=None
) -> datetime.datetime:
    "Returns sunset or sunrise time for a given latitude and longitude, and a particular day"
    if rise_or_set not in ["sunrise", "sunset"]:
        raise ValueError("Can only calculate sunrise or sunset")
    date = date or datetime.datetime.today().date()
    day, month, year = date.day, date.month, date.year

    N1 = math.floor(275 * month / 9)
    N2 = math.floor((month + 9) / 12)
    N3 = 1 + math.floor((year - 4 * math.floor(year / 4) + 2) / 3)
    N = N1 - (N2 * N3) + day - 30
    lngHour = longitude / 15  # longitude in hours

    t = (
        N + ((6 - lngHour) / 24)
        if rise_or_set == "sunrise"
        else N + ((18 - lngHour) / 24)
    )

    M = (0.9856 * t) - 3.289  # Sun's mean anomaly
    L = within(
        M + (1.916 * sin(M)) + (0.020 * sin(2 * M)) + 282.634, 360
    )  # Sun's true longitude
    RA = within(atan(0.91764 * tan(L)), 360)  # Sun's right ascension

    # RA potentially needs to be adjusted into the range [0,360) by adding/subtracting 360
    # right ascension value needs to be in the same quadrant as L

    Lquadrant = (math.floor(L / 90)) * 90
    RAquadrant = (math.floor(RA / 90)) * 90
    RA = (RA + (Lquadrant - RAquadrant)) / 15  # right ascension in hours

    sinDec = 0.39782 * sin(L)  # declination
    cosDec = cos(asin(sinDec))

    cosH = (cos(zenith) - (sinDec * sin(latitude))) / (
        cosDec * cos(latitude)
    )  # local hour angle

    if cosH > 1:
        raise NoSunriseOrSunsetTime("no sunrise")
    if cosH < -1:
        raise NoSunriseOrSunsetTime("no sunset")

    H = (
        360 - acos(cosH) if rise_or_set == "sunrise" else acos(cosH)
    ) / 15  # H in hours
    T = H + RA - (0.06571 * t) - 6.622  # local mean time of rising/setting
    UT = within(T - lngHour, 24)  # UTC adjustment
    hr = int(UT)
    min = round((UT - math.floor(UT)) * 60)

    return datetime.datetime(year, month, day, hr, min, tzinfo=datetime.timezone.utc)


def sunrise(latitude, longitude, date=None) -> datetime.datetime:
    "Returns sunrise time for a given latitude and longitude, and a particular day"
    return suntime("sunrise", latitude, longitude, date)


def sunset(latitude, longitude, date=None) -> datetime.datetime:
    "Returns sunset time for a given latitude and longitude, and a particular day"
    return suntime("sunset", latitude, longitude, date)


def main():
    print(sunset(51.75, -1.25))


if __name__ == "__main__":
    main()
