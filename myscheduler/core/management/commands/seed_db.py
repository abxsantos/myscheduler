from django.contrib.auth.models import User
from django.core.management import BaseCommand


def create_superuser(username: str, password: str) -> tuple[User, bool]:
    user_already_exists_with_username = User.objects.filter(username=username)
    if user_already_exists_with_username.count() == 0:
        return User.objects.create_superuser(username, None, password), True
    return User.objects.filter(username=username).first(), False


class Command(BaseCommand):
    help = "Create initial data into database."

    def add_arguments(self, parser):

        parser.add_argument(
            "--create-super-user", action="store_true", dest="create_super_user", help="Seeds db with a super user"
        )

    def handle(self, *args, **options):
        username = "admin"
        password = "test"

        create_super_user = options["create_super_user"]

        if create_super_user:
            create_superuser(username, password)
