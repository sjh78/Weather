import requests
2
import pandas as pd
3
from io import StringIO
4
 
5
url = "https://www.gov.mb.ca/conservation_fire/Wx-Hour/currentwx.txt"
6
 
7
text = requests.get(url).text
8
 
9
print(text)
