
import requests
import tqdm
from tqdm import tqdm
import json
from cobec_final_sub import get_dbpedia_abstract
from stop import final
from stop import weight

def extract_concepts(text, endpoint="https://api.dbpedia-spotlight.org/en/annotate"):
    """
    Extract concepts from text using DBpedia Spotlight API via POST request.

    :param text: Input text for concept extraction.
    :param endpoint: DBpedia Spotlight API endpoint.
    :return: List of extracted concepts with their URIs and confidence scores, excluding duplicates.
    """
    # Prepare the API request headers
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'  # Specify content type for POST data
    }

    # Prepare the POST data for the DBpedia Spotlight API request
    data = {
        'text': text,
        'confidence': 0.5,  # Optional: Set confidence threshold
        'support': 20       # Optional: Support threshold
    }

    try:
        # Send the POST request to the DBpedia Spotlight API
        response = requests.post(endpoint, headers=headers, data=data)

        # Check for a successful response
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Check if 'Resources' key exists in the response
            if 'Resources' in data:
                concepts = []
                seen_uris = set()  # Create a set to store unique URIs

                for resource in data['Resources']:
                    concept_uri = resource.get('@URI', 'N/A')

                    # Skip the concept if its URI has already been seen
                    if concept_uri in seen_uris:
                        continue

                    # Add the URI to the seen set
                    seen_uris.add(concept_uri)

                    concept_label = resource.get('@surfaceForm', 'N/A')
                    # Safely retrieve confidence score (if available)
                    confidence_score = resource.get('@confidence', 'N/A')

                    concepts.append({
                        'label': concept_label,
                        'uri': concept_uri,
                        'confidence': confidence_score
                    })
                return concepts
            else:
                print("No resources found in the response.")
                print("Response:", json.dumps(data, indent=2))
                return []

        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []

    except Exception as e:
        print(f"An error occurred: {e}")
        return []



    



def cobec_true(filepath)->list:
    print("running")
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            text=file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {filepath} does not exist.")
    except IOError as e:
        raise IOError(f"An error occurred while reading the file: {e}")
    concepts=extract_concepts(text)
    abstract=dict()
    if concepts:
        print("Extracted Concepts:")
        for concept in tqdm(concepts):
            abstract[concept['uri']]=dict()
            abstract[concept['uri']]['abstract']=get_dbpedia_abstract(concept['uri'])
        else:
            print("no concepts found")

    x=weight(abstract=abstract,text=text)
    sorted_by_values = dict(sorted(x.items(), key=lambda item: item[1], reverse=True))
    temp=list()
    for value in sorted_by_values:
        if sorted_by_values[value]>0:
            temp.append(value)
    temp2=list()
    i=1
    for y in temp:
        if i<=10:
            temp2.append(y)
            i=1+i
    try:
        with open(filepath, "a") as file:
            file.write("import_topics"+"\n")
            print(temp2)
            for item in temp2:
                file.write(item + "\n")  # Write each item followed by a newline
        print(f"List has been written to {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
