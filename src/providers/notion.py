import os, json as js, pandas as pd, requests as rq
from dotenv import load_dotenv

load_dotenv()

# ------------ Models
class Entertainment:
    def __init__(self, name):
        self.Name = name
        self.Cover = ""
        self.Status = ""
        self.Is_streaming_now = False
        self.Type = ""

class Book:
    def __init__(self, name):
        self.Name = name
        self.Cover = ""
        self.Status = ""
        self.Language = ""
        self.Summary = ""
        self.Author = ""

class Project:
    def __init__(self, name):
        self.Name = name
        self.Cover = ""
        self.Tech = []
        self.Description = ""

# ------------ General CLasses
class Connection:
    def __init__(self):
        self.__url = ""
        self.__baseUrl = "https://api.notion.com/v1/"
        self.__key = os.environ["NOTION_SECRET"]
        self.__headers = {
            "Authorization": "Bearer " + self.__key,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def set_url(self, url):
        self.__url = self.__baseUrl + url

    def get_headers(self):
        return self.__headers

    def get_key(self):
        return self.__key

    def get_connection(self, url):
        self.set_url(url)
        return self.__url

class Database:
    def __init__(self, database_id):
        self._database = database_id
        self._connection = Connection()
        self._url = ""
        self.default_sort = {"property": "Name", "direction": "ascending"}
        self._data = {
            "sorts": []
        }

    def filter_and_sort(self, filter = None, sort = None):
        if filter is not None:
            self._data["filter"] = filter
        if sort is not None and sort is list:
            for item in sort:
                self._data["sorts"].append(item)
        else:
            self._data["sorts"].append(self.default_sort)

    def build_connection(self, data = None):
        self._url = self._connection.get_connection("databases/" + self._database)
        if data is not None:
            self._url += data
        return self._url

    def request_data(self, data, url = None):
        try:
            if url is None:
                url = self._url
            response = rq.post(url = url, headers = self._connection.get_headers(), json = data);
            if response.status_code == 200:
                json = response.json()
                return json
            else:
                print(response.text)
        except Exception as e:
            print(f"Error: {e}")

    def print_request_url(self):
        print(f"The request was made to: {self._url}")

    def backup_database(self, dataframe, filename):
        try:
            path = os.path.dirname(__file__)
            relative_path = "/Projects/Telegram_Bot/src/assets/"
            full_path = os.path.join(path, relative_path)
            dataframe.to_csv(f"{full_path}/{filename}.csv")
        except Exception as e:
            print(f"Error {e}")

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
                },
            }
        }
        url = self._connection.get_connection("databases/")
        response = self.request_data(database, url)
        print(response)

# ------------ Databases Classes
class Entertainment_DB(Database):
    def __init__(self):
        super().__init__(os.environ["NOTION_DATABASE_ENTERTAINMENT"])

    def get_media(self):
        super().build_connection(data = "/query?")

        try:
            has_more = True  # The default value from the start is True
            data = self._data
            super().print_request_url()
            name, cover, status, type, is_streaming_now = [], [], [], [], [];

            while has_more:
                rp = super().request_data(data)
                data["start_cursor"] = rp["next_cursor"]

                for item in rp["results"]:
                    name.append(item["properties"]["Name"]["title"][0]["text"]["content"])
                    cover.append(item["cover"]["external"]["url"])
                    status.append(item["properties"]["Status"]["status"]["name"])
                    type.append(item["properties"]["Type"]["select"]["name"])
                    is_streaming_now.append(item["properties"]["Streaming now"]["checkbox"])
                has_more = rp["has_more"]

            media = pd.DataFrame(
                {"Name": name, "Cover": cover, "Status": status, "Type": type,
                 "Is_streaming_now": is_streaming_now})
            # media.set_index("Name", inplace=True)

            return media
        except Exception as e:
            print(f"Error: {e}")

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

filter_entertainment =  {
    "or": [
        {
            "property": "Type",
            "select": {
                "equals": "Anime"
            }
        },
        {
            "property": "Type",
            "select": {
                "equals": "Manga"
            }
        }
    ]
}

# jsons = json.dumps(media, indent=4);
# print(jsons);

entertainment = Entertainment_DB()
entertainment.filter_and_sort(filter_entertainment)
data = entertainment.get_media()
print(data.head())
print(data.info())
print(f"Cantidad de contenido en dataframe: {len(data)}")
# entertainment.backup_database(dataframe = data, filename = "Animes")

# parent = os.environ["NOTION_PAGE_TRASH_DATABASES"]
# cover = "https://somoskudasai.com/wp-content/uploads/2023/12/portada_sousou-no-frieren-37.jpg"
# title = "My trash"
# entertainment.create_database(parent, cover, title)

