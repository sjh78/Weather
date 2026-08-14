import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time

# -----------------------------
# Files
# -----------------------------
INPUT_FILE = "ND_station_list.xlsx"
OUTPUT_FILE = "ND_station_list_with_coordinates.csv"

# -----------------------------
# Convert station name to NDAWN URL slug
# -----------------------------
def station_to_slug(name):
    slug = name.lower()

    # Remove distance/direction suffixes
    suffixes = [
        r"\s+\d+[nesw]+$",
        r"\s+\d+[nesw]{2,}$",
        r"\s+\d+$",
        r"\s+[nesw]+$"
    ]

    for pattern in suffixes:
        slug = re.sub(pattern, "", slug)

    slug = slug.replace(".", "")
    slug = slug.replace("'", "")
    slug = slug.replace("&", "and")

    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")

    return slug


# -----------------------------
# Find station-info page
# -----------------------------
def get_station_info_url(station_name):
    slug = station_to_slug(station_name)

    url = f"https://ndawn.ndsu.nodak.edu/current/{slug}.html"

    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        for a in soup.find_all("a", href=True):
            href = a["href"]

            if "station-info.html" in href:
                if href.startswith("http"):
                    return href
                else:
                    return "https://ndawn.ndsu.nodak.edu/" + href.lstrip("/")

    except Exception as e:
        print(f"Unable to find info page for {station_name}: {e}")

    return None


# -----------------------------
# Extract coordinates
# -----------------------------
def extract_coordinates(info_url):
    try:
        r = requests.get(info_url, timeout=20)
        r.raise_for_status()

        text = r.text

        lat_match = re.search(
            r"Latitude:\s*([-\d.]+)",
            text,
            re.IGNORECASE
        )

        lon_match = re.search(
            r"Longitude:\s*([-\d.]+)",
            text,
            re.IGNORECASE
        )

        lat = lat_match.group(1) if lat_match else None
        lon = lon_match.group(1) if lon_match else None

        return lat, lon

    except Exception as e:
        print(f"Coordinate extraction failed: {e}")
        return None, None


# -----------------------------
# Main
# -----------------------------
df = pd.read_excel(INPUT_FILE, engine="openpyxl")

df["Latitude"] = None
df["Longitude"] = None
df["Source_URL"] = None

for i, row in df.iterrows():

    station = str(row["Station"]).strip()

    print(f"Processing {station}")

    info_url = get_station_info_url(station)

    if info_url:

        lat, lon = extract_coordinates(info_url)

        df.at[i, "Latitude"] = lat
        df.at[i, "Longitude"] = lon
        df.at[i, "Source_URL"] = info_url

    time.sleep(1)

df.to_excel(OUTPUT_FILE, index=False)

print()
print("Finished")
print(f"Output saved to {OUTPUT_FILE}")
