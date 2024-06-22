import os

def save_dataframe(self, dataframe, filename):
    try:
        path = os.path.dirname(__file__)
        relative_path = "/Projects/Telegram_Bot/src/assets/"
        full_path = os.path.join(path, relative_path)
        dataframe.to_csv(f"{full_path}/{filename}.csv")
    except Exception as e:
        print(f"Error {e}")