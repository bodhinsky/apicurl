def process_collection(collection):
    if not collection:
        return None
    
    collection_info = []
    for release in collection:
        title = release['basic_information']['title']
        artist = release['basic_information']['artists'][0]['name']
        year = release['basic_information']['year']
        genre = release['basic_information']['genres'][0] if release['basic_information']['genres'] else None
        style = release['basic_information']['styles'][0] if release['basic_information']['styles'] else None
        collection_info.append({
            'Title': title,
            'Artist': artist,
            'Year': year,
            'Genre': genre,
            'Style': style,
        })
    return collection_info