'''main program'''

'''
Run: uvicorn main:app --reload --port 9000
Check: http://127.0.0.1:9000 in your browser
'''

import os
import logging
import pathlib
import hashlib
from fastapi import FastAPI, Form, File, UploadFile, HTTPException, Depends, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from pydantic import BaseModel
from contextlib import asynccontextmanager
import json
from typing import Dict, List


# Define the path to the images & sqlite3 database
images_dir = pathlib.Path(__file__).parent.resolve() / "images"
db = pathlib.Path(__file__).parent.resolve() / "db" / "mercari.sqlite3"
# items_file = pathlib.Path(__file__).parent.resolve() / "data/items.json"

# Ensure directories exist
images_dir.mkdir(parents=True, exist_ok=True)

# def get_items():
#     if not items_file.exists():
#         items_file.parent.mkdir(parents=True, exist_ok=True)
#         save_items({"items": []})

#     with items_file.open("r") as f:
#         return json.load(f)

# def save_items(items):
#     with items_file.open("w") as f:
#         json.dump(items, f, indent=2)

def get_items_from_database(db: sqlite3.Connection):
    cursor = db.cursor()
    query = """
    SELECT items.name, categories.name AS category, image_name
    FROM items
    JOIN categories
    ON items.category_id = categories.id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    items_list = [{"name": name, "category": category, "image_name": image_name} for name, category, image_name in rows]
    result = {"items": items_list}
    cursor.close()

    return result

def get_items_from_database_by_id(id: int, db: sqlite3.Connection) -> Dict[str, List[Dict[str, str]]]:
    cursor = db.cursor()
    query = """
    SELECT items.name, categories.name AS category, image_name
    FROM items
    JOIN categories
    ON items.category_id = categories.id
    WHERE items.id = ?
    """
    cursor.execute(query, (id,))
    rows = cursor.fetchall()
    items_list = [{"name": name, "category": category, "image_name": image_name} for name, category, image_name in rows]
    result = {"items": items_list}
    cursor.close()

    return result



def get_db():
    if not db.exists():
        yield

    conn = sqlite3.connect(db, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    try:
        yield conn
    finally:
        conn.close()




# STEP 5-1: set up the database connection
def setup_database():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    sql_file = pathlib.Path(__file__).parent.resolve() / "db" / "items.sql"
    with open(sql_file, "r") as f:
        cursor.executescript(f.read())
    conn.commit()
    cursor.close()
    conn.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_database()
    yield


app = FastAPI(lifespan=lifespan)

# logger = logging.getLogger("uvicorn")
# logger.level = logging.INFO
'''
Enable logging for debugging
'''
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

images = pathlib.Path(__file__).parent.resolve() / "images"
origins = [os.environ.get("FRONT_URL", "http://localhost:3000")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


class HelloResponse(BaseModel):
    message: str


@app.get("/", response_model=HelloResponse)
def hello():
    return HelloResponse(**{"message": "Hello, world!"})

class AddItemRequest(BaseModel):
    name: str
    category: str

class AddItemResponse(BaseModel):
    message: str

class Item(BaseModel):
    name: str
    category: str
    category_id: int = None
    image_name: str

# class Item(BaseModel):
#     name: str
#     category: str
#     image_name: str
#     category_id: int = None

# @app.get("/items")
# def get_items_list():
#     return get_items()

@app.get("/items")
def get_items(db: sqlite3.Connection = Depends(get_db)):
    return get_items_from_database(db)

# @app.get("/items/{item_id}")
# def get_item(item_id: int):
#     items_data = get_items()
#     if "items" not in items_data or not items_data["items"]:
#         raise HTTPException(status_code=404, detail="Item not found")

#     items = items_data["items"]
#     if item_id < 0 or item_id >= len(items):
#         raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")

#     return items[item_id]

# @app.get("/items/{item_id}")
# def get_item(item_id: int):
#     items_data = get_items_from_database()
#     if "items" not in items_data or not items_data["items"]:
#         raise HTTPException(status_code=404, detail="Item not found")

#     items = items_data["items"]
#     if item_id < 0 or item_id >= len(items):
#         raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")

#     return items[item_id]

@app.get("/items/{item_id}")
def get_item(item_id: int, db: sqlite3.Connection = Depends(get_db)):
    items_data = get_items_from_database_by_id(item_id, db)
    if not items_data["items"]:
        raise HTTPException(status_code=404, detail="Item not found")

    return items_data["items"][int(item_id) - 1]

# add_item is a handler to add a new item for POST /items .
@app.post("/items", response_model=AddItemResponse)
async def add_item(
    name: str = Form(...),
    category: str = Form(...),
    image: UploadFile = File(...),
    db: sqlite3.Connection = Depends(get_db),
):
    if not name:
        raise HTTPException(status_code=400, detail="name is required")
    if not category:
        raise HTTPException(status_code=400, detail="category is required")
    if not image:
        raise HTTPException(status_code=400, detail="image is required")

    image_bytes = await image.read()
    hash_value = hashlib.sha256(image_bytes).hexdigest()
    image_filename = f"{hash_value}.jpg"
    image_path = images_dir / image_filename
    with image_path.open("wb") as f:
        f.write(image_bytes)

    # Query the category table
    cursor = db.cursor()
    query_category = "SELECT id FROM categories WHERE name = ?"
    cursor.execute(query_category, (category,))
    rows = cursor.fetchone()
    if rows is None:
        insert_query_category = "INSERT INTO categories (name) VALUES (?)"
        cursor.execute(insert_query_category, (category,))
        category_id = cursor.lastrowid
    else:
        category_id = rows[0]

    item = Item(name=name, category=category, category_id=category_id, image_name=image_filename)
    # item = Item(name=name, category=category, image_name=image_filename, category_id=category_id)
    insert_item_db(item, db)

    # insert_item(Item(name=name, category=category, image_name=image_filename))
    # insert_item_db(Item(name=name, category_id=category, image_name=image_filename), db)
    return AddItemResponse(**{"message": f"name: {name}, image saved as {image_filename}"})



# get_image is a handler to return an image for GET /images/{filename} .
@app.get("/image/{image_name}")
async def get_image(image_name):
    # Create image path
    image = images_dir / image_name

    if not image_name.lower().endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.debug(f"Image not found: {image}")
        image = images_dir / "default.jpg"

    return FileResponse(image)

@app.get("/search")
def search_keyword(keyword: str = Query(...), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    query = """
    SELECT items.name AS name, categories.name AS category, image_name
    FROM items
    JOIN categories
    ON items.category_id = categories.id
    WHERE items.name LIKE ?
    """
    pattern = f"%{keyword}%"
    cursor.execute(query, (pattern,))
    rows = cursor.fetchall()
    items_list = [{"name": name, "category": category, "image_name": image_name} for name, category, image_name in rows]
    result = {"items": items_list}
    cursor.close()

    return result


# def insert_item(item: Item):
#     # STEP 4-2: add an implementation to store an item
#     items_data = get_items()
#     if "items" not in items_data:
#         items_data["items"] = []

#     items_data["items"].append(item.model_dump())

#     save_items(items_data)

def insert_item_db(item: Item, db: sqlite3.Connection) -> int:
    cursor = db.cursor()
    # # Query the category table
    # query_category = "SELECT id FROM categories WHERE name = ?"
    # cursor.execute(query_category, (item.category,))
    # rows = cursor.fetchone()
    # if rows is None:
    #     insert_query_category = "INSERT INTO categories (name) VALUES (?)"
    #     cursor.execute(insert_query_category, (item.category,))
    #     category_id = cursor.lastrowid
    # else:
    #     category_id = rows[0]

    query = """
    INSERT INTO items (name, category_id, image_name) VALUES (?, ?, ?);
    """
    cursor.execute(query, (item.name, item.category_id, item.image_name))

    db.commit()
    cursor.close()
    return cursor.lastrowid
