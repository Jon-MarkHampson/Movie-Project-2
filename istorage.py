from abc import ABC, abstractmethod

"""
ADD docstrings to everything

Note: you don’t need to implement the functions inside the interface, an interface includes only the functions definitions.
"""


class IStorage(ABC):
    @abstractmethod
    def list_movies(self):
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster, media_type):
        pass

    @abstractmethod
    def delete_movie(self, title):
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        pass
