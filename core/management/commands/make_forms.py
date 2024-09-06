from email.policy import default
from pathlib import Path
from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from django.db.models import Model
from django.apps import apps
from django.conf import settings
from jinja2 import Template
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

    def get_input(self, options):
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
        model = model_options.get(model_key, None)
        return model


    def get_target_app(self, options, app_name):
        app_list = [app.name for app in apps.get_app_configs()]
        app_folders = [folder.name for folder in settings.BASE_DIR.glob("*") if folder.is_dir()]
        # remove apps that are not apps
        app_list = [app for app in app_list if app in app_folders]

        target_app:str = options["targetapp"]
        if not target_app or target_app not in app_list:
            target_app:str = inquirer.list_input("Select the target app", choices=app_list, default=app_name) or ""
        return target_app

    def handle(self, *args: Any, **options: Any) -> str | None:
        model = self.get_input(options)
        if not model:
            return
        target_app = self.get_target_app(options, model._meta.app_label)
        if not target_app:
            return
        app_name = model._meta.app_label
        model_name = model._meta.model_name or ""
        model_name = model_name.title().replace(" ", "")
        model_name_lower = model_name.lower()
        model_name_plural = model._meta.verbose_name_plural or ""
        model_name_plural = model_name_plural.replace(" ", "")
        model_name_plural_lower = model_name_plural.lower()

        base_dir: Path = settings.BASE_DIR

        # create the folders
        init_file = base_dir / target_app / "forms" / "__init__.py"

        stub_file = Path(__file__).parent / "stubs" / "forms.py.jinja2"

        file_to_create = base_dir / target_app / "forms" / f"{model_name_plural_lower}.py"

        # create the folders
        for file in [init_file, file_to_create]:
            file.parent.mkdir(parents=True, exist_ok=True)

        # delete existing files
        file_to_delete = base_dir / target_app / "forms.py"

        for file in [file_to_delete]:
            if file.exists():
                content = file.read_text()
                if "class" in content:
                    print(
                        f"File {file} is not empty. Please move the classes to the module and delete file manually."
                    )
                else:
                    file.unlink()

        if file_to_create.exists():
            print(f'The "{file_to_create}" file already exists!')
            overwrite: bool = inquirer.confirm("Do you want to overwrite it?") or False
            if not overwrite:
                return

        # touch all files
        for file in [init_file, file_to_create]:
            file.touch()

        # create the file
        template = Template(stub_file.read_text())
        file_content = template.render(
            app_name=app_name,
            target_app=target_app,
            model=model,
            model_name=model_name,
            model_name_lower=model_name_lower,
            model_name_plural=model_name_plural,
            model_name_plural_lower=model_name_plural_lower,
        )
        file_to_create.write_text(file_content)
        # # init file
        # import_text = f"\nfrom .{model_name_plural_lower} import {model_name}CreateForm, {model_name}UpdateForm\n"
        # views_init_file_content = init_file.read_text()
        # if import_text not in views_init_file_content:
        #     init_file.write_text(import_text + views_init_file_content)

        print(f"Created forms for {app_name}.{model_name}")
