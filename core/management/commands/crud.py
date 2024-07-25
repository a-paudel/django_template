from pathlib import Path
from typing import Any
from django.core.management.base import BaseCommand
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

            print(f"Invalid app name. Check if app is present in INSTALLED_APPS. Valid apps are: {valid_apps}")

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
            "urls": base_dir / app_name / "urls" / "__init__.py",
        }
        file_stubs = {
            "models": Path(__file__).parent / "stubs" / "models.py.jinja2",
            "forms": Path(__file__).parent / "stubs" / "forms.py.jinja2",
            "views": Path(__file__).parent / "stubs" / "views.py.jinja2",
            "urls": Path(__file__).parent / "stubs" / "urls.py.jinja2",
            "template_layout": Path(__file__).parent / "stubs" / "templates" / "layout.html.jinja2",
            "template_list": Path(__file__).parent / "stubs" / "templates" / "list.html.jinja2",
            "template_detail": Path(__file__).parent / "stubs" / "templates" / "detail.html.jinja2",
            "template_form": Path(__file__).parent / "stubs" / "templates" / "form.html.jinja2",
            "template_delete": Path(__file__).parent / "stubs" / "templates" / "delete.html.jinja2",
            "template_table_partial": Path(__file__).parent / "stubs" / "templates" / "table_partial.html.jinja2",
        }
        files_to_create = {
            "models": base_dir / app_name / "models" / f"{model_name_lower}s.py",
            "forms": base_dir / app_name / "forms" / f"{model_name_lower}s.py",
            "views": base_dir / app_name / "views" / f"{model_name_lower}s.py",
            "urls": base_dir / app_name / "urls" / f"{model_name_lower}s.py",
            "template_layout": base_dir / "jinja" / "layouts" / f"{app_name}.html",
            "template_list": base_dir / "jinja" / app_name / (model_name_lower + "s") / "list.html",
            "template_detail": base_dir / "jinja" / app_name / (model_name_lower + "s") / "detail.html",
            "template_form": base_dir / "jinja" / app_name / (model_name_lower + "s") / "form.html",
            "template_delete": base_dir / "jinja" / app_name / (model_name_lower + "s") / "delete.html",
            "template_table_partial": base_dir
            / "jinja"
            / app_name
            / (model_name_lower + "s")
            / "partials"
            / "table.html",
        }

        # create the folders
        for file in list(init_files.values()) + list(files_to_create.values()):
            file.parent.mkdir(parents=True, exist_ok=True)

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

        # touch all files
        for file in list(init_files.values()) + list(files_to_create.values()):
            file.touch()

        # create the models file
        models_template = Template(file_stubs["models"].read_text())
        models_content = models_template.render(
            app_name=app_name, model_name=model_name, model_name_lower=model_name_lower
        )
        files_to_create["models"].write_text(models_content)
        # models init file
        models_import_text = f"\nfrom .{model_name_lower}s import {model_name}\n"
        models_init_file_content = init_files["models"].read_text()
        if models_import_text not in models_init_file_content:
            init_files["models"].write_text(models_import_text + models_init_file_content)

        # create the forms file
        forms_template = Template(file_stubs["forms"].read_text())
        forms_content = forms_template.render(
            app_name=app_name, model_name=model_name, model_name_lower=model_name_lower
        )
        files_to_create["forms"].write_text(forms_content)
        # forms init file
        forms_import_text = f"\nfrom .{model_name_lower}s import {model_name}CreateForm, {model_name}UpdateForm\n"
        forms_init_file_content = init_files["forms"].read_text()
        if forms_import_text not in forms_init_file_content:
            init_files["forms"].write_text(forms_import_text + forms_init_file_content)

        # create the views file
        views_template = Template(file_stubs["views"].read_text())
        views_content = views_template.render(
            app_name=app_name, model_name=model_name, model_name_lower=model_name_lower
        )
        files_to_create["views"].write_text(views_content)
        # views init file
        views_import_text = f"\nfrom .{model_name_lower}s import {model_name}ListView, {model_name}CreateView, {model_name}DetailView, {model_name}UpdateView, {model_name}DeleteView\n"
        views_init_file_content = init_files["views"].read_text()
        if views_import_text not in views_init_file_content:
            init_files["views"].write_text(views_import_text + views_init_file_content)

        # create the urls file
        urls_template = Template(file_stubs["urls"].read_text())
        urls_content = urls_template.render(
            app_name=app_name, model_name=model_name, model_name_lower=model_name_lower
        )
        files_to_create["urls"].write_text(urls_content)
        # urls init file
        urls_import_text = f"\nfrom .{model_name_lower}s import {model_name}_url_patterns\n"
        urls_init_file_content = init_files["urls"].read_text()
        if urls_import_text not in urls_init_file_content:
            init_files["urls"].write_text(urls_import_text + urls_init_file_content)

        # create the templates
        template_names = [name for name in files_to_create.keys() if name.startswith("template_")]
        for template_name in template_names:
            template = Template(file_stubs[template_name].read_text())
            template_content = template.render(
                app_name=app_name, model_name=model_name, model_name_lower=model_name_lower
            )
            files_to_create[template_name].write_text(template_content)

        print(f"Create CRUD files for {app_name}.{model_name}")
        print("Don't forget to add the urls to the main urls.py file")
