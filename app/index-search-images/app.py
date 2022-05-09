from jina.clients import Client
from docarray import DocumentArray

if __name__ == '__main__':
    print("Opening client - HTTP/8080")
    client = Client(host='localhost', protocol='http', port=8080)
    client.show_progress = True

    print("Converting images from JPG to DocArray")
    indexing_documents = DocumentArray.from_files('./imgs/*.jpg').apply(
        lambda d: d.load_uri_to_image_tensor()
    )

    print("Indexing images - only 20")
    indexed_docs = client.post('/index', inputs=indexing_documents[:20])
    print(f'Indexed Documents: {len(indexed_docs)}')

    print("Querying using the first image")
    query_doc = indexing_documents[0]
    queried_docs = client.post("/search", inputs=[query_doc])

    print("Returned matches")
    matches = queried_docs[0].matches
    print(f'Matched documents: {len(matches)}')
