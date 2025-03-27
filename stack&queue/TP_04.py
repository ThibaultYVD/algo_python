from collections import deque
import requests

class Queue:
    def __init__(self):
        self.queue = deque()
    
    def enqueue(self, article):
        """Ajoute un article à la file."""
        self.queue.append(article)
    
    def dequeue(self):
        """Supprime et retourne l’article le plus ancien."""
        if not self.is_empty():
            return self.queue.popleft()
        return "La file est vide."
    
    def is_empty(self):
        """Vérifie si la file est vide."""
        return len(self.queue) == 0
    
    def size(self):
        """Retourne le nombre d’articles en attente."""
        return len(self.queue)

url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=bfb7f013ab9846ffbd2b529db0775073')

response = requests.get(url)
data = response.json()

queue = Queue()

if 'articles' in data:
    for article in data['articles']:
        queue.enqueue(article['title'])

print(f"Nombre d'articles dans la file: {queue.size()}")

while not queue.is_empty():
    print(f"📰 {queue.dequeue()}")
