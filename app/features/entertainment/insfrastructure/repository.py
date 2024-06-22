from typing import List
from app.features.entertainment.core.models import Entertainment
from app.features.shared.interfaces import IConnection
from app.features.shared.notion_api import ENTERTAINMENT_DB as db, Notion
import requests as rq, json as js

class EntertainmentRepository(Notion):
    def __init__(self, connection : IConnection, database : str = db):
        super().__init__(connection, database)

    def get_media(self) -> List[Entertainment]:
        url = super().build_connection(data = "/query?")
        print(url)

        try:
            has_more : bool = True 
            sort_filter = self._data
            media : List[Entertainment] = []

            while has_more:
                rp = super().request_data(sort_filter)
                sort_filter["start_cursor"] = rp["next_cursor"]

                for item in rp["results"]:
                    content = Entertainment(
                        id = item["id"],
                        name = item["properties"]["Name"]["title"][0]["text"]["content"],
                        cover = item["cover"]["external"]["url"],
                        status = item["properties"]["Status"]["status"]["name"],
                        is_streaming = item["properties"]["Streaming now"]["checkbox"]
                    )
                
                    media.append(content)
                has_more = rp["has_more"]
            return media
        except Exception as e:
            print(f"Error: {e}")

    def update_media(self, page_id : str, properties : dict):
        url : str = self._connection.get_connection("pages/" + page_id)
        try:
            response = rq.patch(url = url, headers = self._connection.get_headers(), json = properties);
            if response.status_code == 200:
                json = response.json()
                # print(js.dumps(json, indent=4))
                
                return json
            else:
                print(response.text)
        except Exception as e:
            print(f"Error: {e}")