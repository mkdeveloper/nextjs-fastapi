from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated, Optional
from ._models import Todos, table_create
from ._database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

table_create()

class TodoBase(BaseModel):
    title: str
    description: str
    completed: bool


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/api/todos")
def create_todo(todo: TodoBase, db: db_dependency):
    new_todo = Todos(title = todo.title, description = todo.description, completed = todo.completed)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return {"message": "Todo created successfully"}


@app.get("/api/todos")
def get_todos(db: db_dependency):
    todos = db.query(Todos).all()
    return todos

@app.get("/api/todos/{todo_id}")
def get_todo(todo_id: int, db: db_dependency):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.put("/api/todos/{todo_id}")
def update_todo(todo_id: int, db: db_dependency, title: Optional[str] = None, des: Optional[str] = None, 
                completed: Optional[bool] = None):
    todo_query = db.query(Todos).filter(Todos.id == todo_id)
    todo_found = todo_query.first()
    if not todo_found:
        raise HTTPException(status_code=404, detail="Todo not found")
   
    if title is not None:
        todo_found.title = title
    if des is not None:
        todo_found.description = des
    if completed is not None:
        todo_found.completed = completed
    db.commit()
    db.refresh(todo_found)
    return {"message": "Todo updated successfully"}


@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int, db: db_dependency):
    todo_query = db.query(Todos).filter(Todos.id == todo_id)
    todo_found = todo_query.first()
    if not todo_found:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_query.delete()
    db.commit()
    return {"message": "Todo deleted successfully"}
