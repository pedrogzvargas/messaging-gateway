from dataclasses import dataclass


@dataclass(frozen=True)
class PageResult[T]:
    page: int
    limit: int
    total: int
    pages: int
    items: list[T]
