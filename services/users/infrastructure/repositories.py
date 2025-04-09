from services.users.domain.models import User, UserModel


class UserRepository:
    def __init__(self, db):
        self.db = db

        
        
    def create_user(self, user: User) -> UserModel:
        user_model = UserModel(**user.dict())
        self.db.session.add(user_model)
        self.db.session.commit()
        return user_model
        
    def get_user_by_id(self, user_id: str) -> UserModel:
        return self.db.session.query(UserModel).filter(UserModel.id == user_id).first()
        
    def update_user(self, user_id: str, user: User) -> UserModel:
        user_model = self.get_user_by_id(user_id)
        if user_model:
            for key, value in user.dict().items():
                setattr(user_model, key, value)
            self.db.session.commit()
        return user_model
        
    def delete_user(self, user_id: str) -> None:
        user_model = self.get_user_by_id(user_id)
        if user_model:
            self.db.session.delete(user_model)
            self.db.session.commit()