from elasticsearch import Elasticsearch
import re
from datetime import datetime

def create_index(elastic_instance, index_name):
        if not elastic_instance.indices.exists(index=index_name):
            elastic_instance.indices.create(index=index_name)
            print(f"Index '{index_name}' created.")
        else:
            print(f"Index '{index_name}' already exists.")

def upload_chat_data_from_txt_file(elastic_instance, file_name, index_name):
    # Load and parse the .txt file
    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            match = re.match(r"\[(\d{2}:\d{2}), (\d{1,2}\.\d{1,2}\.\d{4})] (.*?): (.*)", line)
            if match:
                time_str, date_str, sender, message = match.groups()
                timestamp = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")
                doc = {
                    "timestamp": timestamp.isoformat(),
                    "sender": sender,
                    "message": message
                }
                # Send to Elasticsearch
                #print(doc)
                elastic_instance.index(index=index_name, document=doc)
    print("Done uploading messages to Elasticsearch!")

def delete_all_elements(elastic_instance, index_name):
    elastic_instance.delete_by_query(index=index_name, body={"query": {"match_all": {}}})
    print("Deleted all elements from index: " + index_name)

def get_all_texts_from_index(elastic_instance, index_name):
    response = elastic_instance.search(
        index=index_name,
        body={
            "query": {
                "match_all": {}
            },
            "sort": [
                {"timestamp": {"order": "asc"}}
            ],
            "size": 100
        },
    )
    return response

def get_all_texts_from_author(elastic_instance, index_name, author):
    # Search query to find messages from "Reinhold"
    response = elastic_instance.search(index=index_name, body={
        "query": {
            "match": {
                "sender": author  # Searching for messages from Reinhold
            }
        }
    })
    return response

def get_all_texts_from_year(elastic_instance, index_name, year): 
    start_date = f"{year}-01-01T00:00:00"
    end_date = f"{year + 1}-01-01T00:00:00"

    query = {
        "query": {
            "range": {
                "timestamp": {
                    "gte": start_date,
                    "lt": end_date
                }
            }
        },
        "size": 1000 
    }

    response = elastic_instance.search(index=index_name, body=query)
    return response

def print_elastic_results(results):
    count = results["hits"]["total"]["value"]
    print("Number of hits:", count)
    for hit in results['hits']['hits']:
        print(hit["_source"])

def create_author(
        elastic_instance,
        authors_index,
        name: str,
        author_id: str,
        geschlecht: str,
        muttersprache: str,
        fremdsprachen: list,
        region: str,
        age: int,
        beruf: str
    ):
        doc = {
            "id": author_id,
            "name": name,
            "geschlecht": geschlecht,
            "muttersprache": muttersprache,
            "fremdsprachen": fremdsprachen,
            "region": region,
            "age": age,
            "beruf": beruf
        }

        # Index document
        res = elastic_instance.index(index=authors_index, id=author_id, document=doc)
        print(f"Author {author_id} indexed. Result: {res['result']}")

# Connect to ElasticSearch
elastic_instance = Elasticsearch("http://localhost:9200")

# Check if the connection is successful
if elastic_instance.ping():
    print("Connected to ElasticSearch!")

    authors_index = "authors"
    create_index(elastic_instance, authors_index)
    delete_all_elements(elastic_instance, authors_index)

    create_author(
        elastic_instance,
        authors_index,
        name="Reinhold",
        author_id="1",
        geschlecht="männlich",
        muttersprache="Deutsch",
        fremdsprachen=["Englisch", "Russisch"],
        region="Bayern",
        alter=30,
        beruf="Softwareentwickler"
    )

    #TODOs
    #texttype e.g. whatsapp, e-mail 
    #input e.g. touch/keyboard/swype
    #autocorrect on/off
    #Conversationpartner -> familiy/friend .. how well do they know each other
    
    
    whatsapp_messages_index = "whatsapp-messages"
    create_index(elastic_instance, whatsapp_messages_index)

    delete_all_elements(elastic_instance, whatsapp_messages_index)
    upload_chat_data_from_txt_file(elastic_instance, "whatsapp_chat.txt", whatsapp_messages_index)

    #get and print all texts
    all_texts = get_all_texts_from_index(elastic_instance, whatsapp_messages_index)
    #print_elastic_results(all_texts)

    #get and print all texts from me
    my_messages = get_all_texts_from_author(elastic_instance, whatsapp_messages_index, "Reinhold")
    #print_elastic_results(my_messages)

    #get and print all texts from the year 2024
    messages_from_2024 = get_all_texts_from_year(elastic_instance, whatsapp_messages_index, 2024)
    #print_elastic_results(messages_from_2024)

else:
    print("Failed to connect.")