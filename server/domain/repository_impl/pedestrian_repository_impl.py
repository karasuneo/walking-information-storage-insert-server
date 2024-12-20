from abc import ABCMeta, abstractmethod

from psycopg2.extensions import connection


class PedestrianRepositoryImpl(metaclass=ABCMeta):
    @abstractmethod
    def save(
        self,
        conn: connection,
    ) -> None:
        pass
