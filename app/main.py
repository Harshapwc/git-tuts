from fastapi import FastAPI, HTTPException, status

from app.schemas import ItemCreate, ItemResponse, ItemUpdate
from app.storage import store

app = FastAPI(
    title="Git Tuts API",
    description="REST API for managing items",
    version="1.0.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/items", response_model=list[ItemResponse])
def list_items() -> list[dict[str, str | int]]:
    return store.list_items()


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int) -> dict[str, str | int]:
    item = store.get_item(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
        )
    return item


@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate) -> dict[str, str | int]:
    return store.create_item(payload)


@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, payload: ItemUpdate) -> dict[str, str | int]:
    item = store.update_item(item_id, payload)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
        )
    return item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> None:
    deleted = store.delete_item(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
        )
