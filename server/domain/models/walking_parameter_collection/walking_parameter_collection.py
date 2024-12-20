from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from domain.models.walking_parameter.walking_parameter import WalkingParameter


class WalkingParameterCollection:
    def __init__(
        self,
    ) -> None:
        self.__walking_parameters: list[WalkingParameter] = []

    def get_walking_parameters(
        self,
    ) -> list[WalkingParameter]:
        return self.__walking_parameters

    def add(
        self,
        walking_parameter: WalkingParameter,
    ) -> None:
        self.__walking_parameters.append(walking_parameter)

    def remove(
        self,
        walking_parameter: WalkingParameter,
    ) -> None:
        self.__walking_parameters.remove(walking_parameter)

    def __iter__(
        self,
    ) -> Iterator[WalkingParameter]:
        return iter(self.__walking_parameters)

    def __len__(
        self,
    ) -> int:
        return len(self.__walking_parameters)

    def __getitem__(
        self,
        index: int,
    ) -> WalkingParameter:
        return self.__walking_parameters[index]
