from app.schemas import ItemCreate, ItemUpdate


class ItemStore:
    def __init__(self) -> None:
        self._items: dict[int, dict[str, str | int]] = {}
        self._next_id = 1

    def list_items(self) -> list[dict[str, str | int]]:
        return list(self._items.values())

    def get_item(self, item_id: int) -> dict[str, str | int] | None:
        return self._items.get(item_id)

    def create_item(self, payload: ItemCreate) -> dict[str, str | int]:
        item = {
            "id": self._next_id,
            "name": payload.name,
            "description": payload.description,
        }
        self._items[self._next_id] = item
        self._next_id += 1
        return item

    def update_item(
        self, item_id: int, payload: ItemUpdate
    ) -> dict[str, str | int] | None:
        item = self._items.get(item_id)
        if item is None:
            return None

        if payload.name is not None:
            item["name"] = payload.name
        if payload.description is not None:
            item["description"] = payload.description

        return item

    def delete_item(self, item_id: int) -> bool:
        if item_id not in self._items:
            return False
        del self._items[item_id]
        return True


store = ItemStore()
