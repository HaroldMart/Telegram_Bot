from app.features.entertainment.insfrastructure.repository import EntertainmentRepository as Repository
from app.features.shared.notion_api import ENTERTAINMENT_DB as db, KEY as key, BASE_URL as base_url, HEADERS as headers, Connection

filter_entertainment : dict =  {
    "or": [
        {
            "property": "Name",
            "title": {
                "contains": "Boku no Hero"
            }
        },
        # {
        #     "property": "Type",
        #     "select": {
        #         "equals": "Anime"
        #     }
        # },
        # {
        #     "property": "Type",
        #     "select": {
        #         "equals": "Manga"
        #     }
        # }
    ],
    # "and": [
    
    # ]
}

connection = Connection(base_url, key, headers)
entertainment = Repository(connection, db)
entertainment.filter_and_sort(filter_entertainment)
data = entertainment.get_media()
print(data[0].Name)
print(f"la lista tiene {len(data)} elementos")

# parent = os.environ["NOTION_PAGE_TRASH_DATABASES"]
# cover = "https://somoskudasai.com/wp-content/uploads/2023/12/portada_sousou-no-frieren-37.jpg"
# title = "My trash"
# entertainment.create_database(parent, cover, title)