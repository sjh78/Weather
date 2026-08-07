import requests
2
 
3
url = "https://www.gov.mb.ca/conservation_fire/Wx-Hour/currentwx.txt"
4
 
5
response = requests.get(url)
6
 
7
print(response.text)
