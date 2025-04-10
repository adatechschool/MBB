# services\users\infrastructure\repositories.py

from django.contrib.auth import get_user_model

User = get_user_model()


class UserRepository:
    def update(self, user, data):
        # Si le mot de passe est mis à jour, on le gère via la méthode set_password
        if 'password' in data:
            user.set_password(data.pop('password'))
        # Mise à jour des autres champs
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        user.save()
        return user

    def delete(self, user):
        user.delete()
