from urllib.request import urlopen
2
 
3
url = "https://www.gov.mb.ca/conservation_fire/Wx-Hour/currentwx.txt"
4
 
5
text = urlopen(url).read().decode("utf-8")
6
 
7
with open("currentwx.txt", "w", encoding="utf-8") as f:
8
f.write(text)
9
 
10
print("Downloaded currentwx.txt")
11
print(text[:1000])
