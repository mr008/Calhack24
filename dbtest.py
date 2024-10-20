import chromadb
client = chromadb.Client()
collection = client.get_or_create_collection('fruit')
collection.add(
  ids=['1', '2', '3','4'],
  documents=['apple', 'oranges', 'peach',"strawbrerry"]
)
print(collection.query(query_texts='Georgia', n_results=1))