from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models import UserBook
from app.schemas.user_book import UserBookRead, UserBookUpdateAvailability
from app.crud.user_book import get_my_userbooks, update_userbook_availability, get_userbook, delete_userbook
from app.api.deps import get_db
from app.api.auth import get_current_user
from app.models.user import User
from typing import List

router = APIRouter()


@router.get("/my", response_model=List[UserBookRead])
def my_library(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    userbooks = get_my_userbooks(db, current_user)
    return [
        UserBookRead(
            **ub.__dict__,
            book_title=getattr(ub.book, 'title', None),
            book_author=getattr(ub.book, 'author', None)
        )
        for ub in userbooks
    ]


@router.patch("/{userbook_id}/availability", response_model=UserBookRead)
def set_availability(userbook_id: int, data: UserBookUpdateAvailability, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    userbook = get_userbook(db, userbook_id)
    if not userbook:
        raise HTTPException(status_code=404, detail="UserBook not found")
    if userbook.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your book")
    userbook = update_userbook_availability(db, userbook, data.is_available)
    return UserBookRead(
        **userbook.__dict__,
        book_title=getattr(userbook.book, 'title', None),
        book_author=getattr(userbook.book, 'author', None)
    )


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_library(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    userbook = db.query(UserBook).filter(UserBook.book_id == book_id, UserBook.user_id == current_user.id).first()
    if not userbook:
        raise HTTPException(status_code=404, detail="UserBook not found")
    try:
        delete_userbook(db, userbook, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    return None
