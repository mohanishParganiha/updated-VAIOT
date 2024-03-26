# import requests
# from urllib.parse import quote

# app_id = "R5G7P8-69QK2P28PK"
# base_url = f"http://api.wolframalpha.com/v1/simple?appid={app_id}&i="

# def get_weather(location):
#     query = f'weather in {location}'
#     query = quote(query,safe="")
#     try:
#         response = requests.get(base_url+query)
#     except Exception as e:
#         print(e)
    
#     return response.text()
   

# location = "Bhilai"
# weather = get_weather(location)
# print(weather)
import wolframalpha
app_id = "R5G7P8-69QK2P28PK"
client = wolframalpha.Client(app_id=app_id)
res = client.query("weather in ahiwara")


# for pod in res.pods:
#     for sub in pod.subpods:
#         print(sub.plaintext)

print(next(res.results).text)