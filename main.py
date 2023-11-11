from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return "To see the documentation please open the /docs"


@app.post('/post', response_model=Timestamp, summary='Get Post')
def get_post():
    current_time = datetime.now()
    new_timestamp = Timestamp(id=post_db[-1].id + 1,
                              timestamp=int(round(current_time.timestamp())))
    return new_timestamp


@app.get('/dog', summary='Get Dogs')
def get_dogs() -> List[Dog]:
    return list(dogs_db.values())


@app.post('/dog', response_model=Dog, summary='Create Dog')
def create_dog(dog: Dog):
    if dog.pk in dogs_db:
        raise HTTPException(status_code=404, detail="There is a dog with such ID already")
    else:
        dogs_db.update({dog.pk: dog})
    return dog


@app.get('/dog/{pk}', response_model=Dog, summary='Get Dog By PK')
def get_dog_by_pk(pk: int):
    dog_retrieved = dogs_db.get(pk)
    if dog_retrieved is None:
        raise HTTPException(status_code=404, detail="A dog with this ID isn't found")
    else:
        return dog_retrieved


@app.patch('/dog/{pk}', response_model=Dog, summary='Update Dog')
def update_dog(pk: int, dog: Dog):
    if pk != dog.pk:
        raise HTTPException(status_code=404, detail="A dog's ID is not the same as entered")
    if pk in dogs_db:
        dogs_db.update({dog.pk: dog})
        return dog
    else:
        raise HTTPException(status_code=404, detail="A dog with such ID wasn't found")
