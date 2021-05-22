import logging

from typing import Optional
from typing import Tuple
from typing import TypedDict

from django.contrib.auth.base_user import BaseUserManager

logger = logging.getLogger(__name__)


class ClientDataForCreation(TypedDict):
    id: str
    cpf: str
    username: str


class PersonManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def get_by_id_or_create(self, id: str, **user_data: ClientDataForCreation) -> Tuple["Client", bool]:
        """
        Either retrieves a Person entry or creates a new one.
        """
        created_person_queryset = self.filter(id=id)
        logger.info(f"Checking to see if a user of id: {id}")
        if created_person_queryset.exists():
            logger.info("A user with id: " f"{id} already exists retrieving it!")
            return created_person_queryset.first(), False
        logger.info(f"Creating a new user with id: {id}")
        return (
            self.create(
                id=id,
                cpf=user_data.get("cpf"),
                username=user_data.get("username"),
            ),
            True,
        )

    def get_or_none(self, *args, **kwargs) -> Optional["Client"]:
        """
        Perform the query and return a single object matching the given
        keyword arguments if it exists, None otherwise
        """
        try:
            return self.get(*args, **kwargs)
        except (self.model.MultipleObjectsReturned, self.model.DoesNotExist):
            return None
