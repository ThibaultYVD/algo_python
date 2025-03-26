import requests
import time
from pymongo import MongoClient

API_URL = "https://public-api.meteofrance.fr/public/DPClim/v1/liste-stations/infrahoraire-6m"
API_KEY = "eyJ4NXQiOiJOelU0WTJJME9XRXhZVGt6WkdJM1kySTFaakZqWVRJeE4yUTNNalEyTkRRM09HRmtZalkzTURkbE9UZ3paakUxTURRNFltSTVPR1kyTURjMVkyWTBNdyIsImtpZCI6Ik56VTRZMkkwT1dFeFlUa3paR0kzWTJJMVpqRmpZVEl4TjJRM01qUTJORFEzT0dGa1lqWTNNRGRsT1RnelpqRTFNRFE0WW1JNU9HWTJNRGMxWTJZME13X1JTMjU2IiwidHlwIjoiYXQrand0IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJiYzUzOGY4ZS00YTQ1LTQ0NzMtOTRmMC1iOTk1MzY0MmM4NDUiLCJhdXQiOiJBUFBMSUNBVElPTiIsImF1ZCI6IlBFZXRJeklJYlozYVFzQTJZaktJaXRlWGxRUWEiLCJuYmYiOjE3NDI5OTYzMzQsImF6cCI6IlBFZXRJeklJYlozYVFzQTJZaktJaXRlWGxRUWEiLCJzY29wZSI6ImRlZmF1bHQiLCJpc3MiOiJodHRwczpcL1wvcG9ydGFpbC1hcGkubWV0ZW9mcmFuY2UuZnJcL29hdXRoMlwvdG9rZW4iLCJleHAiOjE3NDI5OTk5MzQsImlhdCI6MTc0Mjk5NjMzNCwianRpIjoiYjA5MDEzYzEtNWQ1Mi00NTliLWFjZjItYmJlNzg2MmQwNDQ0IiwiY2xpZW50X2lkIjoiUEVldEl6SUliWjNhUXNBMllqS0lpdGVYbFFRYSJ9.rH4Y35b-tPW4ELVB-APpnN8h0xvEGicHwQbkPjFBOLOrJG4fusI83ExSV7QVRn2-IppPuswNtu1q-H9KSVws7vYArvinDa02q0jIpA9rQH5Lyh_pAM-shwaIzR1aaLqQQnxxqj1f_-bj6q59KJfgpeOS4V4AlVKEv4RF7nK8az-fgpHXLShE2508vPHAGbDhNxPwvpJkxHXQEKNITjmTJ3acdf7OFDnxmQu9c2TqlWRB4Z4BBk52MmQrQb3SfeFb8mMWK9W7blwN4zoxUaNVknRjDLImSUcf1Wp_aUa2Zk_9Qr2ri5VnkDt6tEMwaeTyGsZbZinq391IZ1MPUAqYTA"
headers = {
    "Authorization": f"Bearer {API_KEY}" 
}

params = {
    "id-departement": "35", 
    "parametre": "temperature"
}

response = requests.get(API_URL, headers=headers, params=params)
data = response.json()

if response.status_code == 200:
    data = response.json()
    print("✅ Données récupérées avec succès !")
else:
    print(f"❌ Erreur {response.status_code}: {response.text}")

villes = [{"id": station["id"], "nom": station["nom"], "latitude": station["lat"], "longitude": station["lon"]} for station in data]

client = MongoClient("mongodb://localhost:27017/")
db = client["weatherDB"]
collection = db["data"]
collection.insert_many(villes)

def quick_sort(arr, key):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x[key] < pivot[key]]
    middle = [x for x in arr if x[key] == pivot[key]]
    right = [x for x in arr if x[key] > pivot[key]]
    return quick_sort(left, key) + middle + quick_sort(right, key)

def measure_time(sort_func, arr, key):
    arr_copy = arr.copy()
    start = time.time()
    sort_func(arr_copy, key)
    end = time.time()
    return (end - start) * 1000

def binarySearch(array, targetValue, key):
    leftIndex = 0
    rightIndex = len(array) - 1

    while leftIndex <= rightIndex:
        currentIndex = (leftIndex + rightIndex) // 2
        currentValue = array[currentIndex][key]

        if currentValue == targetValue:
            return currentIndex
        
        if currentValue < targetValue:
            leftIndex = currentIndex + 1
        else:
            rightIndex = currentIndex - 1

    return -1

data_list = list(collection.find({}, {"_id": 0}))
critere = "latitude" 

targetValue = 48.584833

toto = quick_sort(data_list, critere)
print(toto)
seachResult = binarySearch(toto, targetValue, critere)

quick_time = measure_time(quick_sort, data_list, critere)



if seachResult != -1:
    print("Value",targetValue,"found at index", seachResult)
else:
    print("Target not found in array.")

print("\nTemps d'exécution des algorithmes:")
print(f"Quick Sort : {quick_time:.2f} ms")