from fastapi import Depends, FastAPI, HTTPException, Request, Response, Query
from sqlalchemy.orm import Session
from . import models

from . import schemas
from .database import SessionLocal, engine
from dotenv import load_dotenv


from fastapi.middleware.cors import CORSMiddleware
import uuid

from . import crud

import csv
from datetime import datetime

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


origins = [
    "http://localhost:5173",
    "https://electiongpt.org"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
async def hello_word():
    return "Yo! Hello world, The backend is running !!!"


@app.post("/api/create/journalist-exchange/", response_model=schemas.Journalist)
async def create_journalist_exchange(response:Response, request:Request,
 journalist: schemas.JournalistCreate, db: Session = Depends(get_db), override_limit: bool = False 
):
    request_count = int(request.cookies.get("counter","0"))
    print("override_limit : ", override_limit)
    if not override_limit and request_count >= 5:
        raise HTTPException(status_code=429, detail="Request limit exceeded")
    request_count += 1
    print("request_count : ", request_count)
    response.set_cookie(key="counter", value=str(request_count))
    return crud.create_journalist_exchange(db=db, journalist=journalist)


@app.get("/api/journalist-exchange/{exchange_id}", response_model=schemas.Journalist)
async def read_journalist_exchange(exchange_id: int, db: Session = Depends(get_db)):
    db_user = crud.read_journalist_exchange(db, exchange_id=exchange_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="journalist-exchange not found")
    return db_user


# @app.put("/api/update/journalist-exchange/response/{exchange_id}", response_model=schemas.Journalist)
# def update_journalist_exchange_response(
#     journalist_id: int,
#     response: str,
#     db: Session = Depends(get_db)
# ):
#     journalist = crud.update_journalist_exchange_response(db, journalist_id, response)
#     if not journalist:
#         raise HTTPException(status_code=404, detail="journalist-exchange not found")
#     return journalist


@app.put(
    "/api/update/journalist-exchange/rating/{exchange_id}",
    response_model=schemas.Journalist,
)
async def update_journalist_exchange_rating(
    exchange_id: int, rating: str, db: Session = Depends(get_db)
):
    journalist = crud.update_journalist_exchange_rating(db, exchange_id, rating)
    if not journalist:
        raise HTTPException(status_code=404, detail="journalist-exchange not found")
    return journalist


@app.post("/api/create/developer-exchange/", response_model=schemas.Developer)
async def create_developer_exchange(
    developer: schemas.DeveloperCreate, db: Session = Depends(get_db)
):
    return crud.create_developer_exchange(db=db, developer=developer)


@app.get("/api/developer-exchange/{exchange_id}", response_model=schemas.Developer)
async def read_developer_exchange(exchange_id: int, db: Session = Depends(get_db)):
    db_user = crud.read_developer_exchange(db, exchange_id=exchange_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="developer-exchange not found")
    return db_user


@app.put(
    "/api/update/developer-exchange/upvote_Response/{exchange_id}",
    response_model=schemas.Developer,
)
async def update_developer_exchange_upvote_response(
    exchange_id: int, upvote_response: str, db: Session = Depends(get_db)
):
    developer = crud.update_developer_exchange_upvote_response(
        db, exchange_id, upvote_response
    )
    if not developer:
        raise HTTPException(status_code=404, detail="developer-exchange not found")
    return developer


@app.put(
    "/api/update/developer-exchange/correct_query/{exchange_id}",
    response_model=schemas.Developer,
)
async def update_developer_exchange_correct_query(
    exchange_id: int, correct_query: str, db: Session = Depends(get_db)
):
    developer = crud.update_developer_exchange_correct_query(
        db, exchange_id, correct_query
    )
    if not developer:
        raise HTTPException(status_code=404, detail="developer-exchange not found")
    return developer


@app.post("/api/create/developer-exchange/", response_model=schemas.Developer)
async def create_developer_exchange(
    developer: schemas.DeveloperCreate, db: Session = Depends(get_db)
):
    return crud.create_developer_exchange(db=db, developer=developer)

@app.post("/api/save-form-data")
async def store_data(data: schemas.FormData):
    return crud.store_data(data = data)


# class JournalistQueryResponse(BaseModel):
#     query_id: uuid.UUID = Field(default_factory=uuid.uuid4)
#     query: str
#     responses: list[dict] = []

# class DeveloperQueryResponse(BaseModel):
#     query_id: uuid.UUID = Field(default_factory=uuid.uuid4)
#     query: str
#     responses: list[dict] = []
#     query_inputs: list[str] = []

# journalist_mode_table = []

# developer_mode_table = []

# def find_element_index(list, target_id):
#     for index, item in enumerate(list):
#         if item["query_id"] == target_id:
#             return index
#     return -1

# @app.post("/api/new-query-response")
# def create_new_query_response(query: str, mode: str):
#     new_query_id = uuid.uuid4()
#     print("new_query_id : ",new_query_id)
#     if(mode=="journalist"):
#         generated_response = "generated response for the journalist query"
#         new_record = JournalistQueryResponse(query_id=new_query_id, query=query, responses=[{"value": generated_response, "rating": "block"}])
#         journalist_mode_table.append(new_record.model_dump())
#         print("journalist_mode_table : ", journalist_mode_table)
#         return journalist_mode_table
#     elif(mode=="developer"):
#         generated_response = "generated response for the developer query"
#         new_record = DeveloperQueryResponse(query_id=new_query_id, query=query, responses=[{"value": generated_response, "rating": "block"}],query_inputs=[])
#         developer_mode_table.append(new_record.model_dump())
#         return developer_mode_table
#     else:
#         raise HTTPException(status_code=400, detail="Invalid mode.")


# @app.put("/api/regenerate-response")
# def regenerate_query_response(query_id: uuid.UUID, mode: str):
#     if(mode=="journalist"):
#         lst = journalist_mode_table
#     elif(mode=="developer"):
#         lst = developer_mode_table
#     else:
#         raise HTTPException(status_code=400, detail="Invalid mode.")
#     query_index = find_element_index(lst, query_id)

#     if query_index == -1:
#         raise HTTPException(status_code=404, detail="Query ID not found.")

#     regenerated_response = "regenerated response for journalist query" if mode == "journalist" else "regenerated response for developer query"
#     new_response = {"value": regenerated_response, "rating": "block"}
#     lst[query_index]["responses"].append(new_response)
#     return lst


# @app.put("/api/rate-journalist-query")
# def rate_journalist_query(query_id: uuid.UUID, response_index:int, rating: str):
#         query_index = find_element_index(journalist_mode_table,query_id)
#         if query_index == -1:
#             raise HTTPException(status_code=404, detail="Query ID not found.")
#         if response_index>=len(journalist_mode_table[query_index]["responses"]) or response_index<0:
#             raise HTTPException(status_code=400, detail="Invalid response index.")
#         if(rating!="upvoted" and rating!="downvoted"):
#             raise HTTPException(status_code=400, detail="Invalid rating.")
#         journalist_mode_table[query_index]["responses"][response_index]["rating"] = rating
#         return journalist_mode_table


# @app.put("/api/upvote-developer-query")
# def upvote_developer_query(query_id: uuid.UUID, response_index:int):
#         query_index = find_element_index(developer_mode_table,query_id)
#         if query_index == -1:
#             raise HTTPException(status_code=404, detail="Query ID not found.")
#         if response_index>=len(developer_mode_table[query_index]["responses"]) or response_index<0:
#             raise HTTPException(status_code=400, detail="Invalid response index.")
#         textual_response = "textual response in response to the upvote"
#         new_response = {"value": textual_response,
#         "rating": "none",}
#         developer_mode_table[query_index]["responses"].insert(response_index+1, new_response)
#         return developer_mode_table


# @app.put("/api/downvote-developer-query")
# def downvote_developer_query(query_id: uuid.UUID, response_index:int, query_entered:str):
#         query_index = find_element_index(developer_mode_table,query_id)
#         if query_index == -1:
#             raise HTTPException(status_code=404, detail="Query ID not found.")
#         if response_index>=len(developer_mode_table[query_index]["responses"]) or response_index<0:
#             raise HTTPException(status_code=400, detail="Invalid response index.")
#         print("length : ", len(developer_mode_table[query_index]["responses"]))
#         print("response_index : ", response_index)
#         developer_mode_table[query_index]["query_inputs"].append(query_entered)
#         developer_mode_table[query_index]["responses"][response_index]["rating"] = "downvoted"
#         return developer_mode_table
