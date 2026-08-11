from urllib.request import urlopen
import csv

# Download Manitoba weather file
url = "https://www.gov.mb.ca/conservation_fire/Wx-Hour/currentwx.txt"

text = urlopen(url).read().decode("utf-8")

# Save a copy for troubleshooting
with open("currentwx.txt", "w", encoding="utf-8") as f:
    f.write(text)

# Split into lines
lines = text.splitlines()

# Find beginning of data
data_start = 0

for i, line in enumerate(lines):
    if "---" in line:
        data_start = i + 1
        break

# Parse weather rows
records = []

for line in lines[data_start:]:
    line = line.strip()

    if not line:
        continue

    parts = line.split()

    if len(parts) < 17:
        continue

    records.append(parts)
# Load station coordinates

station_lookup = {}

with open("station_coordinates.csv", newline="", encoding="utf-8") as coordfile:

    reader = csv.DictReader(coordfile)

    for row in reader:

        station_lookup[row["Station"].strip()] = {
            "Full": row["Full"],
            "Latitude": row["Latitude"],
            "Longitude": row["Longitude"]
        }
# Export clean CSV

with open("weather.csv", "w", newline="", encoding="utf-8") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Station",
        "Full",
        "Latitude",
        "Longitude",
        "Date",
        "Hour",
        "Temperature",
        "RH",
        "WindDirDegrees",
        "WindDirCompass",
        "WindSpeed",
        "WindSpeedMax",
        "Rain1Hr",
        "Rain24Hr",
        "TempMax",
        "TempMin",
        "RHMax",
        "RHMin"
    ])

    for row in records:

                station = row[0]

        coords = station_lookup.get(station, {})

        writer.writerow([
            station,
            coords.get("Full", ""),
            coords.get("Latitude", ""),
            coords.get("Longitude", ""),
            f"{row[1]} {row[2]} {row[3]}",
            row[4],
            row[5],
            row[6],
            row[7],
            row[8],
            row[9],
            row[10],
            row[11],
            row[12],
            row[13],
            row[14],
            row[15],
            row[16]
        ])

print("Rows parsed:", len(records))
