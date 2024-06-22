class Entertainment:
    def __init__(self, id : str, name : str, cover : str, status : str, is_streaming : bool) -> None:
        self.Id : str = id
        self.Name : str = name
        self.Cover : str = cover
        self.Status : str = status
        self.Is_streaming_now = is_streaming

class Anime(Entertainment):
    def __init__(self, id : str, name : str, cover : str, status : str, is_streaming : bool) -> None:
        super().__init__(id, name, cover, status, is_streaming, "Anime")

class Movie(Entertainment):
    def __init__(self, id : str, name : str, cover : str, status : str, is_streaming : bool) -> None:
        super().__init__(id, name, cover, status, is_streaming, "Movie")

class Serie(Entertainment):
    def __init__(self, id : str, name : str, cover : str, status : str, is_streaming : bool) -> None:
        super().__init__(id, name, cover, status, is_streaming, "Serie")

class Manga(Entertainment):
    def __init__(self, id : str, name : str, cover : str, status : str, is_streaming : bool) -> None:
        super().__init__(id, name, cover, status, is_streaming, "Manga")

class Cartoon(Entertainment):
    def __init__(self, id : str, name : str, cover : str, status : str, is_streaming : bool) -> None:
        super().__init__(id, name, cover, status, is_streaming, "Cartoon")