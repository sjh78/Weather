from urllib.request import urlopen
2
import csv
3
 
4
# Download Manitoba weather file
5
url = "https://www.gov.mb.ca/conservation_fire/Wx-Hour/currentwx.txt"
6
 
7
text = urlopen(url).read().decode("utf-8")
8
 
9
# Save a copy for troubleshooting
10
with open("currentwx.txt", "w", encoding="utf-8") as f:
11
f.write(text)
12
 
13
# Split into lines
14
lines = text.splitlines()
15
 
16
# Find beginning of data
17
data_start = 0
18
 
19
for i, line in enumerate(lines):
20
if "---" in line:
21
data_start = i + 1
22
break
23
 
24
# Parse weather rows
25
records = []
26
 
27
for line in lines[data_start:]:
28
line = line.strip()
29
 
30
if not line:
31
continue
32
 
33
parts = line.split()
34
 
35
if len(parts) < 8:
36
continue
37
 
38
records.append(parts)
39
 
40
# Export simple CSV
41
with open("weather.csv", "w", newline="", encoding="utf-8") as csvfile:
42
 
43
writer = csv.writer(csvfile)
44
 
45
writer.writerow([
46
"Station",
47
"Field2",
48
"Field3",
49
"Field4",
50
"Field5",
51
"Field6",
52
"Field7",
53
"Field8"
54
])
55
 
56
for row in records:
57
writer.writerow(row[:8])
58
 
59
print("Rows parsed:", len(records))
