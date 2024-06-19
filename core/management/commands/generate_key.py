from pathlib import Path
from typing import Any
from django.core.management import BaseCommand
import secrets
import shutil
import re


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        # check if .env file exists
        env_file = Path(".env")
        secret = secrets.token_urlsafe(100)

        if not env_file.exists():
            print(".env file does not exist. Copying default env file")
            shutil.copyfile(".env.example", env_file)

        line = f"DJANGO_SECRET_KEY={secret}\n"
        # replace the line with DJANGO_SECRET_KEY with above line
        text = env_file.read_text()
        pattern = r"DJANGO_SECRET_KEY=.*\n"
        num_matches = len(re.findall(pattern, text))
        if num_matches:
            text = re.sub(r"DJANGO_SECRET_KEY=.*\n", line, text)
            env_file.write_text(text)
        else:
            env_file.write_text(text + "\n" + line)
