from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from django.core.management import call_command
from django.conf import settings
from django.db import transaction
from faker import Faker

from users.models import User


Faker.seed(0)
fake = Faker()


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force seed, even if not in debug mode",
            default=False,
        )
        return super().add_arguments(parser)

    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> str | None:
        if not settings.DEBUG and not options["force"]:
            return "Seed is only available in debug mode. Use --force to force seed"

        if options["force"]:
            call_command("flush", "--noinput")
        else:
            call_command("flush")

        # create models here
        User.objects.create_user("test@example.com", "password")
