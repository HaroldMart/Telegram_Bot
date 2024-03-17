import os, json as js, pandas as pd, requests as rq;
from dotenv import load_dotenv;
from models import Entertainment;
from utils import Connection as conn;

load_dotenv();
KEY = os.environ["NOTION_SECRET"];

def get_entertainment(filter = None, sort = None):
    connection = conn(KEY);
    url = connection.get_connection("databases/" + os.environ["ENTERTAINMENT_PAGE_NOTION"] + "/query?");
    print(f"The request was made to: {url}");

    def get_data_json(json):
        data = {};
        for item in json["results"]:
            name = item["properties"]["Name"]["title"][0]["text"]["content"]
            media = Entertainment(
                name=item["properties"]["Name"]["title"][0]["text"]["content"],
                cover=item["cover"]["external"]["url"],
                status=item["properties"]["Status"]["status"]["name"],
                is_streaming_now=item["properties"]["Streaming now"]["checkbox"],
                type=item["properties"]["Type"]["select"]["name"],
            )
            object = media.__dict__
            data.update({f"{name}": object});
        return data;

    def create_dataframe(media):
        name, cover, status, type, is_streaming_now = [], [], [], [], [];

        for value in media.values():
            name.append(value["Name"]);
            cover.append(value["Cover"]);
            status.append(value["Status"]);
            type.append(value["Type"]);
            is_streaming_now.append(value["Is_streaming_now"]);

        info = pd.DataFrame({"Name": name, "Cover": cover, "Status": status, "Type": type, "Is_streaming_now": is_streaming_now});
        info.set_index("Name", inplace=True);
        print(info.head(20))

    def get_data(data):
        try:
            response = rq.post(url=url, headers=connection.get_headers(), json=data);
            if response.status_code == 200:
                json = response.json();
                return json;
            else:
                print(response.text)
        except Exception as e:
            print(f"Error: {e}");

    default_sort = { "property": "Name", "direction": "ascending" }
    data = {
        "sorts": []
    }

    if filter is not None:
        data["filter"] = filter;

    if sort is not None and type(sort) is list:
        for item in sort:
            data["sorts"].append(item)
    else:
        data["sorts"].append(default_sort)

    try:
        has_more = True; # The default value from the start is True
        media = {}

        while has_more:
            rp = get_data(data)
            data["start_cursor"] = rp["next_cursor"];
            media.update(get_data_json(rp));
            has_more = rp["has_more"];

        print(f"Total of entertainment data in the list: {len(media)}");
    except Exception as e:
        print(f"Error: {e}");






filter =  {
        "property": "Type",
        "select": {
            "equals": "Anime"
        }
};

get_entertainment(filter = filter);

# jsons = json.dumps(media, indent=4);
# print(jsons);

# data = {
#     "filter": {
#         "property": "Type",
#         "select": {
#             "equals": "Anime"
#         }
#         # "or": [
#         #     {
#         #
#         #     }
#         # ]
#     },
#     "sorts": [
#         default_sort
#     ]
# }