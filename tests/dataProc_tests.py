from apiCurl.dataProcessing import process_collection

collection_path = 'data/testCollection.json'

if os.path.exists(collection_path):
    with open(collection_path) as json_file:
        collection = json.load(json_file)

def test_process_data():
    assert not process_collection(collection)==[]
