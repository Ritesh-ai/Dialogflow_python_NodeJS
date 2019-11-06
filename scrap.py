import requests
import re

# API_ENDPOINT = "http://127.0.0.1:8001"

# data = {
# 	"names":"how to do the image classification using python wikipedia"
# }

# r = requests.post(url = API_ENDPOINT, data = data) 

# data = r.json()

# print(data)


def scrapping(text):
    print("Text=============================",text)
    data = data = {
                "names":text
                }
    r = requests.post(url = "http://127.0.0.1:8001", data = data)

    return r.json()

print(scrapping("What is Numpy in Python"))