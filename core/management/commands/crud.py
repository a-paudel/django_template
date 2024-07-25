from pathlib import Path
from textwrap import dedent
from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from django.conf import settings
from jinja2 import Template


class Command(BaseCommand):
    def get_app(self) -> str:
        while True:
            app = input("Enter the name of the app:\n")
            valid_apps = [
                app
                for app in settings.INSTALLED_APPS
                if app
                not in [
                    "django.contrib.admin",
                    "django.contrib.auth",
                    "django.contrib.contenttypes",
                    "django.contrib.sessions",
                    "django.contrib.messages",
                    "whitenoise.runserver_nostatic",
                    "django.contrib.staticfiles",
                    "django_vite",
                    "debug_toolbar",
                    "django_rq",
                    "django_rq_email_backend",
                    "core",
                    "users",
                ]
            ]

            if app in valid_apps:
                return app

            print(f"Invalid app name. Valid apps are: {valid_apps}")

    def get_model(self) -> str:
        while True:
            model = input("Enter the name of the model:\n")
            if model:
                return model.title()

    def handle(self, *args: Any, **options: Any) -> str | None:
        app_name = self.get_app()
        model_name = self.get_model()
        model_name_lower = model_name.lower()

        base_dir: Path = settings.BASE_DIR

        # create the folders
        init_files = {
            "models": base_dir / app_name / "models" / "__init__.py",
            "forms": base_dir / app_name / "forms" / "__init__.py",
            "views": base_dir / app_name / "views" / "__init__.py",
        }

        for file in init_files.values():
            file.parent.mkdir(parents=True, exist_ok=True)
            if not file.exists():
                file.touch()

        # define the stubs
        file_stubs = {
            "models": Path(__file__).parent / "stubs" / "models.py.jinja2",
            "forms": Path(__file__).parent / "stubs" / "forms.py.jinja2",
        }

        # delete existing files
        files_to_delete = [
            base_dir / app_name / "models.py",
            base_dir / app_name / "views.py",
            base_dir / app_name / "forms.py",
        ]
        for file in files_to_delete:
            if file.exists():
                content = file.read_text()
                if "class" in content:
                    print(f"File {file} is not empty. Please move the classes to the module and delete file manually.")
                else:
                    file.unlink()

        # create the files
        files_to_create = {
            "models": base_dir / app_name / "models" / f"{model_name_lower}s.py",
            "forms": base_dir / app_name / "forms" / f"{model_name_lower}s.py",
        }

        existing_files = []
        for file in files_to_create.values():
            if file.exists():
                existing_files.append(file)

        if existing_files:
            print("The following files already exist:")
            for file in existing_files:
                print(file)
            while True:
                overwrite = input("Do you want to overwrite them? (y/N)\n") or "n"
                overwrite = overwrite.lower()[0]
                if overwrite not in ["y", "n"]:
                    print("Invalid input. Please enter 'y' or 'n'")
                    continue
                if overwrite == "n":
                    return
                break

        # create the models file
        models_template = Template(file_stubs["models"].read_text())
        models_content = models_template.render(model_name=model_name)
        files_to_create["models"].write_text(models_content)
        # add imports to __init__.py
        models_import_text = f"\nfrom .{model_name_lower}s import {model_name}\n"
        models_init_file_content = init_files["models"].read_text()
        if models_import_text not in models_init_file_content:
            init_files["models"].write_text(models_import_text + models_init_file_content)

        # create the forms file
        forms_template = Template(file_stubs["forms"].read_text())
        forms_content = forms_template.render(app_name=app_name, model_name=model_name)
        files_to_create["forms"].write_text(forms_content)
        # add imports to __init__.py
        forms_import_text = f"\nfrom .{model_name_lower}s import {model_name}CreateForm, {model_name}UpdateForm\n"
        forms_init_file_content = init_files["forms"].read_text()
        if forms_import_text not in forms_init_file_content:
            init_files["forms"].write_text(forms_import_text + forms_init_file_content)
