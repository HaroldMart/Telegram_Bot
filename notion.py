import requests as rq
from app.features.shared.notion_api import Notion


class Books_DB(Database):
    def __init__(self):
        super().__init__(os.environ["NOTION_DATABASE_BOOKS"])

    def get_books(self):
        super().build_connection(data = "/query?")

        try:
            has_more = True  # The default value from the start is True
            data = self._data
            super().print_request_url()
            name, cover, status, language, summary, author = [], [], [], [], [], []

            while has_more:
                rp = super().request_data(data)
                data["start_cursor"] = rp["next_cursor"]

                for item in rp["results"]:
                    name.append(item["properties"]["Name"]["title"][0]["text"]["content"])
                    cover.append(item["cover"]["external"]["url"])
                    status.append(item["properties"]["Status"]["select"]["name"])
                    language.append(item["properties"]["Language"]["select"]["name"])

                    author_data = item["properties"]["Author"]["rich_text"]
                    summary_data = item["properties"]["What i understand"]["rich_text"]

                    summary.append(summary_data[0]["text"]["content"]) if len(summary_data) > 0 else summary.append("Empty")
                    author.append(author_data[0]["text"]["content"]) if len(author_data) > 0 else author.append("Empty")

                has_more = rp["has_more"]

            books = pd.DataFrame(
                {"Name": name, "Cover": cover, "Status": status, "Language":
                    language, "Author": author, "Summary": summary})
            print(name)
            # books.set_index("Name", inplace=True)

            return books
        except Exception as e:
            print(f"Error: {e}")

class Projects_DB(Database):
    def __init__(self):
        super().__init__(os.environ["NOTION_DATABASE_PROJECTS"])

    def get_projects(self):
        super().build_connection(data="/query?")

        try:
            has_more = True  # The default value from the start is True
            projects = None
            data = self._data
            super().print_request_url()
            name, cover, description, tech = [], [], [], []

            while has_more:
                rp = super().request_data(data)
                data["start_cursor"] = rp["next_cursor"]

                for item in rp["results"]:
                    name.append(item["properties"]["Name"]["title"][0]["text"]["content"])
                    cover.append(item["cover"]["external"]["url"])

                    description_data = item["properties"]["Description"]["rich_text"]
                    tech_data = item["properties"]["Tech"]["multi_select"]

                    description.append(description[0]["text"]["content"]) if len(description_data) > 0 else description.append("Empty")
                    if len(tech_data) > 0:
                        list_tech = []
                        for item in tech_data:
                            list_tech.append(item["name"])
                        tech.append(list_tech)
                    else:
                        tech.append("Empty")

                projects = pd.DataFrame(
                    {"Name": name, "Cover": cover, "Description": description, "Tech": tech})
                # projects.set_index("Name", inplace=True)

                has_more = rp["has_more"]
            return projects
        except Exception as e:
            print(f"Error: {e}")


def create_database(self, parent, cover, title):
        # Is in progress
        database = {
            "parent": {
                "type": "page_id",
                "page_id": parent
            },
            "icon": {
                "type": "emoji",
                "emoji": "📝"
            },
            "cover": {
                "type": "external",
                "external": {
                    "url": cover
                }
            },
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": title,
                        # "link": 'null'
                    }
                }
            ],
            "properties": {
                "Name": {
                    "title": {}
                },
                "Description": {
                    "rich_text": {}
                },
                "In stock": {
                    "checkbox": {}
                },
                "Food group": {
                    "select": {
                        "options": [
                            {
                                "name": "🥦Vegetable",
                                "color": "green"
                            },
                            {
                                "name": "🍎Fruit",
                                "color": "red"
                            },
                            {
                                "name": "💪Protein",
                                "color": "yellow"
                            }
                        ]
                    }
                },
                "Price": {
                    "number": {
                        "format": "dollar"
                    }
                },
                "Last ordered": {
                    "date": {}
                },
                "Store availability": {
                    "type": "multi_select",
                    "multi_select": {
                        "options": [
                            {
                                "name": "Duc Loi Market",
                                "color": "blue"
                            },
                            {
                                "name": "Rainbow Grocery",
                                "color": "gray"
                            },
                            {
                                "name": "Nijiya Market",
                                "color": "purple"
                            },
                            {
                                "name": "Gus'\''s Community Market",
                                "color": "yellow"
                            }
                        ]
                    }
                }
            }
        }

        response = self.request_data(database, self._connection.get_connection("databases/"))
        print(response)













            #     for item in rp["results"]:
            #         # ids = item["id"]
            #         id.append(item["id"])
            #         name.append(item["properties"]["Name"]["title"][0]["text"]["content"])
            #         cover.append(item["cover"]["external"]["url"])
            #         status.append(item["properties"]["Status"]["status"]["name"])
            #         type.append(item["properties"]["Type"]["select"]["name"])
            #         is_streaming_now.append(item["properties"]["Streaming now"]["checkbox"])
            #     has_more = rp["has_more"]

            # media = pd.DataFrame(
            #     {"ID": id, "Name": name, "Cover": cover, "Status": status, "Type": type,
            #      "Is_streaming_now": is_streaming_now})\
                 

      # media.set_index("Name", inplace=True)

            # super().update_page_properties(ids, {
            #     "properties":
            #         {
            #             "Name": {
            #                 "title": [
            #                     {
            #                         "text": {
            #                             "content": "Boku no Hero Academia (Season 7)"
            #                         }
            #                     }
            #                 ]
            #             }
            #         }
            # })


# print(data.head())
# print(data.info())
# print(f"Cantidad de contenido en dataframe: {len(data)}")
# entertainment.backup_database(dataframe = data, filename = "Animes")