from typing import Awaitable, Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

Decorator = Callable[[Callable[P, R]], Callable[P, R]]

NoReturnDecorator = Callable[[Callable[P, None]], Callable[P, None]]

AsyncDecorator = Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]
