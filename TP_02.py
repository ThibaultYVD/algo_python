import requests
import time
from pymongo import MongoClient

API_URL = "https://public-api.meteofrance.fr/public/DPClim/v1/liste-stations/infrahoraire-6m"
API_KEY = "eyJ4NXQiOiJOelU0WTJJME9XRXhZVGt6WkdJM1kySTFaakZqWVRJeE4yUTNNalEyTkRRM09HRmtZalkzTURkbE9UZ3paakUxTURRNFltSTVPR1kyTURjMVkyWTBNdyIsImtpZCI6Ik56VTRZMkkwT1dFeFlUa3paR0kzWTJJMVpqRmpZVEl4TjJRM01qUTJORFEzT0dGa1lqWTNNRGRsT1RnelpqRTFNRFE0WW1JNU9HWTJNRGMxWTJZME13X1JTMjU2IiwidHlwIjoiYXQrand0IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJiYzUzOGY4ZS00YTQ1LTQ0NzMtOTRmMC1iOTk1MzY0MmM4NDUiLCJhdXQiOiJBUFBMSUNBVElPTiIsImF1ZCI6IlBFZXRJeklJYlozYVFzQTJZaktJaXRlWGxRUWEiLCJuYmYiOjE3NDI5ODU2ODYsImF6cCI6IlBFZXRJeklJYlozYVFzQTJZaktJaXRlWGxRUWEiLCJzY29wZSI6ImRlZmF1bHQiLCJpc3MiOiJodHRwczpcL1wvcG9ydGFpbC1hcGkubWV0ZW9mcmFuY2UuZnJcL29hdXRoMlwvdG9rZW4iLCJleHAiOjE3NDI5ODkyODYsImlhdCI6MTc0Mjk4NTY4NiwianRpIjoiYTY0Yzc0NTYtNDRiOC00NDc2LWFlMmQtMjAwNTA5MzQwZTU0IiwiY2xpZW50X2lkIjoiUEVldEl6SUliWjNhUXNBMllqS0lpdGVYbFFRYSJ9.WGhexJndeAz-Sbh5tnjYyNwNCNi5rJHFniqm6rdqu1mHarqX9_v0mDF2kXceMlzPlCnYBpPcTj1YZ9u0Qv5JHQG-iB0F1xDQYr3dxadOMyT2AAeoA62KjxuwyH-QL_nVEtmAIwwoiGTOtbmXiwCIitQYy8A9Rfb1zPLGbKacW8BHWiOJmeMq0xZvxeLArcAC4gRlRh3KCP3WWFK95m0eG4CJwFUE0YZ6fuhDsutQCYEn-H3mm2j3C_OHhFhVoZZbA-nLJRO1e22XfjpS8IqZAgKnrfGSHCMDmj4Gf3kY99VtThPtQUzonqMpGCY3NvjcGVj5l-z8PJdCI6sH4qtokg"  # Remplacez par votre clé API
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
    print(data)
else:
    print(f"❌ Erreur {response.status_code}: {response.text}")

villes = [{"id": station["id"], "nom": station["nom"], "latitude": station["lat"], "longitude": station["lon"]} for station in data]

print("Données récupérées:", villes)

client = MongoClient("mongodb://localhost:27017/")
db = client["weatherDB"]
collection = db["data"]
collection.insert_many(villes)

print(collection)
print("✅ Données insérées dans MongoDB !")

def bubble_sort(arr, key):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j][key] > arr[j+1][key]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

def selection_sort(arr, key):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j][key] < arr[min_idx][key]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

def insertion_sort(arr, key):
    for i in range(1, len(arr)):
        key_value = arr[i]
        j = i - 1
        while j >= 0 and key_value[key] < arr[j][key]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_value

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

data_list = list(collection.find({}, {"_id": 0}))
critere = "latitude" 

bubble_time = measure_time(bubble_sort, data_list, critere)
selection_time = measure_time(selection_sort, data_list, critere)
insertion_time = measure_time(insertion_sort, data_list, critere)
quick_time = measure_time(quick_sort, data_list, critere)

print("\nTemps d'exécution des algorithmes:")
print(f"Bubble Sort : {bubble_time:.2f} ms")
print(f"Selection Sort : {selection_time:.2f} ms")
print(f"Insertion Sort : {insertion_time:.2f} ms")
print(f"Quick Sort : {quick_time:.2f} ms")

best_algo = min([(bubble_time, "Bubble Sort"), (selection_time, "Selection Sort"),
                 (insertion_time, "Insertion Sort"), (quick_time, "Quick Sort")], key=lambda x: x[0])

print(f"\n🚀 Algorithme le plus rapide: {best_algo[1]} avec {best_algo[0]:.2f} ms")
