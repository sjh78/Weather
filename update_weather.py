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

    if len(parts) < 8:
        continue

    records.append(parts)

# Export simple CSV
with open("weather.csv", "w", newline="", encoding="utf-8") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Station",
        "Field2",
        "Field3",
        "Field4",
        "Field5",
        "Field6",
        "Field7",
        "Field8"
    ])

    for row in records:
        writer.writerow(row[:8])

print("Rows parsed:", len(records))
