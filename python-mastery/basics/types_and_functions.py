"""Types and functions."""

from datetime import datetime
from json import dumps
from typing import Callable, Dict, List, Literal, Optional, TypeVar, Union

from pydantic.dataclasses import dataclass

UserId = int
UserName = str
UserEmail = str
UserStatus = Literal["ACTIVE", "INACTIVE", "DELETED"]


@dataclass
class User:
    """
    User class.

    Attributes:
        id (UserId): The user's ID.
        name (UserName): The user's name.
        email (UserEmail): The user's email.
        created_at (datetime): The date and time when the user was created.
        updated_at (Optional[datetime]): The date and time when the user was last updated.
            Defaults to None.
        phone_number (Optional[str]): The user's phone number. Defaults to None.
        is_active (bool): Indicates if the user is active. Defaults to True.
        status (UserStatus): The user's status. Defaults to "ACTIVE".
    """
    id: UserId
    name: UserName
    email: UserEmail
    created_at: datetime
    updated_at: Optional[datetime] = None
    phone_number: Optional[str] = None
    is_active: bool = True
    status: UserStatus = "ACTIVE"

    def to_dict(self) -> Dict[str, Union[str, int, bool]]:
        """
        Convert user to dictionary representation.

        Returns:
            Dict[str, Union[str, int, bool]]: A dictionary representing the user's attributes.
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at is not None else "",
            "is_active": self.is_active,
            "status": self.status,
            "phone_number": self.phone_number if self.phone_number is not None else "",
        }


T = TypeVar("T")


def find_first(
    items: List[T],
    predicate: Callable[[T], bool],
) -> Optional[T]:
    """Find first item matching predicate."""
    for item in items:
        if predicate(item):
            return item
    return None


def main() -> None:
    """Main function."""
    users: List[User] = [
        User(
            id=1,
            name="Alice",
            email="alice@example.com",
            created_at=datetime.now(),
            phone_number="1234567890",
            is_active=True,
            status="ACTIVE",
            updated_at=datetime.now(),
        ),
        User(
            id=2,
            name="Bob",
            email="bob@example.com",
            created_at=datetime.now(),
            is_active=False,
            phone_number="0987654321",
            status="INACTIVE",
            updated_at=datetime.now(),
        ),
    ]

    # Find active users
    active_user = find_first(
        users,
        lambda user: user.is_active,
    )
    # get user which has phone number and is active
    user_with_phone_number = find_first(
        users, lambda user: user.is_active and user.phone_number is not None
    )

    if active_user:
        print(f"Found active user: {dumps(active_user.to_dict(), indent=4)}")
    else:
        print("No active users found")
    if user_with_phone_number:
        print(
            f"Found user with phone number: {dumps(user_with_phone_number.to_dict(), indent=4)}"
        )
    else:
        print("No user with phone number found")


if __name__ == "__main__":
    main()
