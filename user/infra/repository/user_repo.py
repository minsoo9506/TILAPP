from fastapi import HTTPException

from database import SessionLocal
from user.domain.repository.user_repo import IUserRepository
from user.domain.user import User
from user.infra.db_models.user import User as UserModel
from utils.db_utils import row_to_dict


class UserRepository(IUserRepository):
    def save(self, user: User) -> None:
        new_user = UserModel(
            id=user.id,
            email=user.email,
            name=user.name,
            password=user.password,
            created_at=user.created_at,
            updated_at=user.updated_at,
            memo=user.memo,
        )

        with SessionLocal() as db:
            try:
                db = SessionLocal()
                db.add(new_user)
                db.commit()
            finally:
                db.close()

    def find_by_email(self, email: str) -> User:
        with SessionLocal() as db:
            try:
                db = SessionLocal()
                user = db.query(UserModel).filter(UserModel.email == email).first()
                if not user:
                    raise HTTPException(status_code=422, detail="User not found")
            finally:
                db.close()

        return User(**row_to_dict(user))

    def find_by_id(self, id: str) -> User:
        with SessionLocal() as db:
            db = SessionLocal()
            user = db.query(UserModel).filter(UserModel.id == id).first()
            if not user:
                raise HTTPException(status_code=422, detail="User not found")

        return User(**row_to_dict(user))

    def update(self, user_vo: User) -> User:
        with SessionLocal() as db:
            db = SessionLocal()
            user = db.query(UserModel).filter(UserModel.id == user_vo.id).first()
            if not user:
                raise HTTPException(status_code=422, detail="User not found")
            user.name = user_vo.name
            user.password = user_vo.password
            db.add(user)
            db.commit()
        return user

    def get_users(self, page: int, items_per_page: int) -> tuple[int, list[User]]:
        with SessionLocal() as db:
            db = SessionLocal()
            query = db.query(UserModel)
            total_count = query.count()
            offset = (page - 1) * items_per_page
            users = query.limit(items_per_page).offset(offset).all()
            user_list = [User(**row_to_dict(user)) for user in users]
        return total_count, user_list

    def delete_user(self, id: str) -> None:
        with SessionLocal() as db:
            db = SessionLocal()
            user = db.query(UserModel).filter(UserModel.id == id).first()
            if not user:
                raise HTTPException(status_code=422, detail="User not found")
            db.delete(user)
            db.commit()
