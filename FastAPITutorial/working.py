from fastapi import FastAPI, Path, Query, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None
class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None
inventory = {}

@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item to delete", gt=0)):
    if item_id not in inventory:
        # return {"Error": "ID does not exists."}
        raise HTTPException(status_code=404, detail="Item ID does not exists.")
    del inventory[item_id]
    return {"Success": "Item deleted!"}

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        # return {"Error": "Item ID does not exists."}
        raise HTTPException(status_code=404, detail="Item ID does not exists.")
    if item.name != None:
        inventory[item_id].name = item.name
    if item.price != None:
        inventory[item_id].price = item.price
    if item.brand != None:
        inventory[item_id].brand = item.brand
    return inventory[item_id]

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        # return {"Error": "Item ID already exists."}
        raise HTTPException(status_code=400, detail="Item ID already exists.")
    inventory[item_id] = item
    return inventory[item_id]

@app.get("/get-by-name")
def get_item(name: str = Query(None, title="Name", description="Name of item.", min_length=2, max_length=10)):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    # return {"Data": "Not found!"}
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    raise HTTPException(status_code=400, detail="Item name not found.")

@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="The ID of the item you'd like to view.", gt=0)):
    return inventory[item_id]

