

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.db.db import get_tasks, add_task, delete_task
class TodoCreate(BaseModel):
    note: str
router=APIRouter()
router = APIRouter(prefix="/api")
@router.get("/todos")
async def getTodos():
     return await get_tasks()
@router.post("/todos/add")
async def addTodo(todo: TodoCreate):
    try:
        new_task = await add_task(todo.note)
        return new_task
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@router.delete("/delete/{todoId}")
async def deleteTodo(todoId: int):
      return await delete_task(todoId)
