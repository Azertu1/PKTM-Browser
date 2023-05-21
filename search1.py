import re
import requests
from bs4 import BeautifulSoup
import socks
import socket

class SearchEngine:
    def __init__(self):
        self.documents = []

    def add_document(self, document):
        self.documents.append(document)

    def crawl_and_index(self, start_url, max_pages=10):
        visited_urls = set()
        queue = [start_url]
        count = 0

        # Setup Tor SOCKS proxy
        socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
        socket.socket = socks.socksocket

        while queue and count < max_pages:
            url = queue.pop(0)

            if url not in visited_urls:
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        content = response.text
                        self.add_document(content)
                        visited_urls.add(url)
                        count += 1

                        # Extract links from the page and add them to the queue
                        soup = BeautifulSoup(content, 'html.parser')
                        links = soup.find_all('a', href=True)
                        for link in links:
                            new_url = link['href']
                            if new_url.startswith('http') or new_url.startswith('https'):
                                queue.append(new_url)
                except requests.exceptions.RequestException:
                    print(f"Failed to crawl: {url}")
    
    def search(self, query):
        results = []
        for document in self.documents:
            if self._match_query(document, query):
                results.append(document)
        return results

    def _match_query(self, document, query):
        query_words = re.findall(r'\b\w+\b', query.lower())
        document_words = re.findall(r'\b\w+\b', document.lower())
        for word in query_words:
            if word not in document_words:
                return False
        return True

# Usage example
search_engine = SearchEngine()

# Crawl and index .onion webpages using Tor
search_engine.crawl_and_index("http://example.onion", max_pages=10)

# Searching for documents
results = search_engine.search("sample query")
for document in results:
    print(document)