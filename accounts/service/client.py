# accounts\service\client.py

"""Client module for interacting with the Accounts microservice API."""

import requests
from django.conf import settings

from common.dtos import AccountDTO


class AccountClient:
    """HTTP client for interacting with the Accounts microservice."""

    BASE_URL = settings.ACCOUNTS_SERVICE_URL.rstrip("/")

    def get_account(self, user_id: int) -> AccountDTO:
        """Retrieve account information for the given user ID.

        Args:
            user_id: The unique identifier of the user account to retrieve.

        Returns:
            AccountDTO: Data transfer object containing the account information.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """
        resp = requests.get(
            f"{self.BASE_URL}/api/accounts/get/account/",
            params={"user_id": user_id},
        )
        resp.raise_for_status()
        data = resp.json()["data"]
        return AccountDTO(**data)

    def update_account(
        self,
        user_id: int,
        username: str,
        email: str,
        bio: str = None,
        profile_picture: str = None,
    ) -> AccountDTO:
        """Update account information for the given user ID.

        Args:
            user_id: The unique identifier of the user account to update.
            username: The new username for the account.
            email: The new email address for the account.
            bio: Optional biography text for the user profile.
            profile_picture: Optional URL to the user's profile picture.

        Returns:
            AccountDTO: Data transfer object containing the updated account information.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """
        payload = {
            "username": username,
            "email": email,
            "bio": bio,
            "profile_picture": profile_picture,
        }
        resp = requests.put(
            f"{self.BASE_URL}/api/accounts/update/account/",
            params={"user_id": user_id},
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()["data"]
        return AccountDTO(**data)

    def delete_account(self, user_id: int) -> None:
        """Delete account for the given user ID.

        Args:
            user_id: The unique identifier of the user account to delete.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """
        resp = requests.delete(
            f"{self.BASE_URL}/api/accounts/delete/account/",
            params={"user_id": user_id},
        )
        resp.raise_for_status()
