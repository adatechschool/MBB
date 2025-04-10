# services\users\application\services.py

from services.users.infrastructure.repositories import UserRepository


class UserService:
    def __init__(self, repository=None):
        self.repository = repository if repository else UserRepository()

    def update_account(self, user, data):
        """
        Met à jour les informations du compte utilisateur.
        """
        return self.repository.update(user, data)

    def delete_account(self, user):
        """
        Supprime le compte utilisateur.
        """
        self.repository.delete(user)
