latitude = 51.75  # Put your own coordinates here!
longitude = -1.25

DEG_TO_RAD = math.pi / 180

zenith = 90.8
now = datetime.datetime.now()
day, month, year = now.day, now.month, now.year


def within(val, upper):
    if val < 0:
        return val + upper
    elif val >= upper:
        return val - upper
    else:
        return val


sin = lambda degrees: math.sin(DEG_TO_RAD * degrees)
cos = lambda degrees: math.cos(DEG_TO_RAD * degrees)
tan = lambda degrees: math.tan(DEG_TO_RAD * degrees)

asin = lambda val: math.asin(val)
acos = lambda val: math.acos(val)
atan = lambda val: math.atan(val)

# first calculate the day of the year

N1 = math.floor(275 * month / 9)
N2 = math.floor((month + 9) / 12)
N3 = 1 + math.floor((year - 4 * math.floor(year / 4) + 2) / 3)
N = N1 - (N2 * N3) + day - 30

# convert the longitude to hour value and calculate an approximate time

lngHour = longitude / 15

# if rising time is desired:
# t = N + ((6 - lngHour) / 24)  # sunrise
t = N + ((18 - lngHour) / 24)  # sunset

# calculate the Sun's mean anomaly

M = (0.9856 * t) - 3.289

# calculate the Sun's true longitude

L = within(M + (1.916 * sin(M)) + (0.020 * sin(2 * M)) + 282.634, 360)

# calculate the Sun's right a9scension

RA = within(atan(0.91764 * tan(L)), 360)

# RA potentially needs to be adjusted into the range [0,360) by adding/subtracting 360

# right ascension value needs to be in the same quadrant as L

Lquadrant = (math.floor(L / 90)) * 90
RAquadrant = (math.floor(RA / 90)) * 90
RA = RA + (Lquadrant - RAquadrant)

# right ascension value needs to be converted into hours

RA = RA / 15

# calculate the Sun's declination

sinDec = 0.39782 * sin(L)
cosDec = cos(asin(sinDec))

# calculate the Sun's local hour angle

cosH = (cos(zenith) - (sinDec * sin(latitude))) / (cosDec * cos(latitude))

if cosH > 1:
    print("the sun never rises on this location (on the specified date)")
    sys.exit(1)
if cosH < -1:
    print("the sun never sets on this location (on the specified date)")
    sys.exit(1)

# finish calculating H and convert into hours

# H = 360 - acos(cosH)  # sunrise
H = acos(cosH)  # sunset

H = H / 15

# calculate local mean time of rising/setting

T = H + RA - (0.06571 * t) - 6.622

# adjust back to UTC

UT = within(T - lngHour, 24)
hr = int(UT)
min = round((UT - math.floor(UT)) * 60)

sunset_time = datetime.datetime(year, month, day, hr, min, tzinfo=datetime.timezone.utc)
print(sunset_time)
