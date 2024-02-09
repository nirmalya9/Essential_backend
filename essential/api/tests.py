import requests

# payload = {
#     'username':'lucifer.rex',
#     'content':'oh shit, new post'
# }
# file = open('img3.jpg','rb')
# file_path = 'img3.jpg'
# files = {"image":(file_path,file)}

response = requests.get("http://127.0.0.1:8000/post/view")

print(response.json())