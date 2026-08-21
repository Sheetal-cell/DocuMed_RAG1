import requests
response=requests.get(
    "http://127.0.0.1:8000/graph",
    json={"question": "What are the relationships between hypertension and stroke?"}
      )
print("Graph API response:", response.json())
