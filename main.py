from fastapi import FastAPI, Query
from enum import Enum
from typing import Optional
from pydantic import BaseModel

## Additionaly added "Enum" value provides a swagger dropdown.
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

##U can find this model assigned to the API schema. Down below the queries 
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app  = FastAPI()

## Cute little if statement. Just to assign the message to the model name. 
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, 
                "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, 
                "message": "LeCNN all the images"}

    return {"model_name": model_name, 
            "message": "Have some residuals"}

## Just the basic opening root point
@app.get("/")
async def root():
    return {"message": "Hello World"}

## path to item within all items     
# @app.get("/items/{item_id}")
# async def read_item(item_id):
#     return {"item_id": item_id}

# ## item_id declared to be an int 
# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}

## Assigment of /me/ value to dispaly particular message  
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "It's you dummy!"}

## Displaying users 
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

## filepath:path provided in the current path ables us to inserting the desired path into ours. 
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

## setting up a limit of values to display.
# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]

## Accept of setting up the item_id value. We also adding the q optional value.
## below example of curl request
## curl -X 'GET' \
##   'http://127.0.0.1:8000/items/98?q=siema' \
##   -H 'accept: application/json'
# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: Optional[str] = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}

##Apart from passing the item_id we also passed the q value and a bool at the end of the path
##Be sides we can pass a default value in case the bool {short} value was ommited.
##example below:
##curl -X 'GET' \
##'http://127.0.0.1:8000/items/Ajdi?q=Dodatkowa%20warto%C5%9B%C4%87&short=true' \
##-H 'accept: application/json'
##
# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item

## Combination of /users/, /items/ with all /items/ elements 
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
                user_id: int, 
                item_id: str, 
                q: Optional[str] = None, 
                short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

## needy is now the mandatory input argument. We are getting an error if we not pass the needy value.
# @app.get("/items/{item_id}")
# async def read_user_item(   
#             item_id: str, 
#             needy: str):
#     item = {"item_id": item_id, "needy": needy}
#     return item

##In this case, there are 3 query parameters:
## needy, a required str.
## skip, an int with a default value of 0.
## limit, an optional int.
# @app.get("/items/{item_id}")
# async def read_user_item(
#     item_id: str, needy: str, skip: int = 0, limit: int | None = None
# ):
#     item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
#     return item

## Based on the item Model declared above only two values are mandatory. Rest can be omitted. 
# @app.post("/items/")
# async def create_item(item: Item):
#     return item

## Function is addind the price to the tax and serving an additonal parameter price_with_tax.
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

##
# @app.put("/items/{item_id}")
# async def create_item(item_id: int, item: Item):
#     return {"item_id": item_id, **item.dict()}


@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

## q parameter is optional with default items assigned. 
# @app.get("/items/")
# async def read_items(q: Optional[str] = None):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

## we have provided a mex lenght for the q parameter. 
@app.get("/items/")
async def read_items(q: Optional[str] = Query(None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


