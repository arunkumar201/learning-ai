from dataclasses import dataclass
from datetime import datetime
from json import dumps
from typing import Callable, Dict, List, Optional, TypeVar, Union

UserId = int
UserName = str
UserEmail = str


@dataclass
class User:
    id: UserId
    name: UserName
    email: UserEmail
    created_at: datetime
    phone_number: Optional[str] = None
    is_active: bool = True

    def to_dict(self) -> Dict[str, Union[str, int, bool]]:
        """Convert user to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active,
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
    users: List[User] = [
        User(
            id=1,
            name="Alice",
            email="alice@example.com",
            created_at=datetime.now(),
            # phone_number="1234567890",
            is_active=True,
        ),
        User(
            id=2,
            name="Bob",
            email="bob@example.com",
            created_at=datetime.now(),
            is_active=False,
            phone_number="0987654321",
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
