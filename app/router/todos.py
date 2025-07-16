from fastapi import APIRouter

router=APIRouter()
router = APIRouter(prefix="/api")
@router.get("/todos")
def getTodos():
     return [
        {"id": 1, "title": "Zrobić zakupy"},
        {"id": 2, "title": "Napisać raport"}
    ]