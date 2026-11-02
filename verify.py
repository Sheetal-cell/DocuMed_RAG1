import requests
response=requests.get(
    "${API_BASE_URL}/graph",
    json={"question": "What are the relationships between hypertension and stroke?"}
      )
print("Graph API response:", response.json())
