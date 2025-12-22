from typing import Awaitable, Callable, ParamSpec, TypeAlias, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

Decorator = Callable[[Callable[P, R]], Callable[P, R]]

NoReturnDecorator = Callable[[Callable[P, None]], Callable[P, None]]

AsyncDecorator = Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]

# JSON
JSONType: TypeAlias = dict[str, "JSONType"] | list["JSONType"] | str | int | float | bool | None
JSONObject: TypeAlias = dict[str, JSONType]
JSONArray: TypeAlias = list[JSONType]
