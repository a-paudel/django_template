from random import choices
from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from django.core.management import call_command
from django.db.models import Model
from django.apps import apps
from django.conf import settings
import inquirer



class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--model", type=str, help="The model in app.model format.", required=False
        )
        parser.add_argument(
            "--targetapp", type=str, help="The app to create the CRUD files in.", required=False,
        )
        return super().add_arguments(parser)

    def get_model_key(self, options):
        # try get model from arguments
        model = options["model"]
        if model:
            # check if model is valid
            appname, modelname = model.split(".")
            try:
                model = apps.get_model(appname, modelname)
            except LookupError:
                print(f"Model {appname}.{modelname} not found.")
                return
            return model

        apps_to_skip = [
            "admin",
            "contenttypes",
            "users",
            "auth",
            "sessions",
            "django_rq",
        ]
        model_options: dict[str, type[Model]] = {}
        for appname, modeldict in apps.all_models.items():
            if appname in apps_to_skip:
                continue
            for modelname, model in modeldict.items():
                model_options[f"{appname}.{modelname}"] = model
        if not model_options:
            print(
                "No valid models found. Check the INSTALLED_APPS setting and models.py files."
            )
            return
        model_key: str = (
            inquirer.list_input("Select the model", choices=model_options) or ""
        )
        return model_key

    def get_target_app(self, options):
        app_list = [app.name for app in apps.get_app_configs()]
        app_folders = [folder.name for folder in settings.BASE_DIR.glob("*") if folder.is_dir()]
        # remove apps that are not apps
        app_list = [app for app in app_list if app in app_folders]

        target_app = options["targetapp"]
        if not target_app or target_app not in app_list:
            target_app = inquirer.list_input("Select the target app", choices=app_list) or ""
        return target_app

    def handle(self, *args: Any, **options: Any) -> str | None:
        model_key = self.get_model_key(options)
        if not model_key:
            return
        target_app = self.get_target_app(options)
        if not target_app:
            return



        call_command("make_forms", model=model_key)
        call_command("make_views", model=model_key)
        call_command("make_templates", model=model_key)
        call_command("make_urls", model=model_key)
