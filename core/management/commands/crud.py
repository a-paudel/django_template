from pathlib import Path
from textwrap import dedent
from typing import Any
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("model", type=str, help="Name of the model to create in app.Model foramt")

    def handle(self, *args: Any, **options: Any) -> str | None:
        model_input = options["model"]
        if "." not in model_input:
            return "Model name should be in app.Model format"
        model_parts = model_input.split(".")
        if len(model_parts) != 2:
            return "Model name should be in app.Model format"
        app = model_parts[0].lower()
        model = model_parts[1].title()

        app_init_file = Path(".") / app / "__init__.py"
        if not app_init_file.exists():
            return f"App {app} does not exist"

        self.create_model(app, model)
        self.create_forms(app, model)
        self.create_views(app, model)
        self.create_templates(app, model)

    def create_model(self, app: str, model: str):
        # create models file if not exists
        model_file = Path(".") / app / "models.py"
        if not model_file.exists():
            model_file.write_text("")

        # check if file has imports
        models_import_lines = ["from django.db import models", "from core.models import BaseModel"]
        for import_line in models_import_lines:
            models_file_text = model_file.read_text()
            if import_line not in models_file_text:
                model_file.write_text(f"{import_line}\n" + models_file_text)

        # check if model already exists
        models_file_text = model_file.read_text()
        if f"class {model}" in models_file_text:
            print(f"Model {model} already exists")
        else:
            # add model to models file
            model_class_text = dedent(f"""
            class {model}(BaseModel):
                '''Model definition for {model}.'''

                class Meta:
                    '''Meta definition for {model}.'''

                    verbose_name = '{model}'
                    verbose_name_plural = '{model}s'

                def __str__(self):
                    pass
            """)
            model_file.write_text(models_file_text + model_class_text)

    def create_forms(self, app: str, model: str):
        forms_init_file = Path(".") / app / "forms" / "__init__.py"
        if not forms_init_file.exists():
            forms_init_file.parent.mkdir(parents=True, exist_ok=True)
            forms_init_file.write_text("")

        form_file = Path(".") / app / "forms" / f"{model.lower()}.py"
        if not form_file.exists():
            form_file.write_text("")

        import_lines = [
            "from django import forms",
            "from core.forms import BaseForm",
            f"from {app}.models import {model}",
        ]
        for import_line in import_lines:
            text = form_file.read_text()
            if import_line not in text:
                form_file.write_text(f"{import_line}\n" + text)

        # check if forms already exist
        form_file_text = form_file.read_text()
        # create form
        if f"class {model}CreateForm" in form_file_text:
            print(f"{model}CreateForm already exists")
        else:
            create_form_text = dedent(f"""
                class {model}CreateForm(BaseForm, forms.ModelForm):
                    class Meta:
                        model = {model}
                        fields = "__all__"
                """)
            form_file.write_text(form_file_text + create_form_text)

        # check if forms already exist
        form_file_text = form_file.read_text()
        # create form
        if f"class {model}UpdateForm" in form_file_text:
            print(f"{model}UpdateForm already exists")
        else:
            update_form_text = dedent(f"""
                class {model}UpdateForm(BaseForm, forms.ModelForm):
                    class Meta:
                        model = {model}
                        fields = "__all__"
                """)
            form_file.write_text(form_file_text + update_form_text)

    def create_views(self, app: str, model: str):
        views_init_file = Path(".") / app / "views" / "__init__.py"
        if not views_init_file.exists():
            views_init_file.parent.mkdir(parents=True, exist_ok=True)
            views_init_file.write_text("")

        view_file = Path(".") / app / "views" / f"{model.lower()}.py"
        if not view_file.exists():
            view_file.write_text("")

        import_lines = [
            "from typing import Any",
            "from django.db.models.query import QuerySet",
            "from django.urls import reverse",
            "from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView",
            f"from {app}.models import {model}",
            f"from {app}.forms.{model.lower()} import {model}CreateForm, {model}UpdateForm",
        ]
        for import_line in import_lines:
            text = view_file.read_text()
            if import_line not in text:
                view_file.write_text(f"{import_line}\n" + text)

        # list view
        view_file_text = view_file.read_text()
        if f"class {model}ListView(ListView):" in view_file_text:
            print("ListView already exists")
        else:
            view_file.write_text(
                view_file_text
                + dedent(f"""
            class {model}ListView(ListView):
                model = {model}
                template_name = "{model.lower()}s/list.html"
                paginate_by = 10

            """)
            )
        # create view
        view_file_text = view_file.read_text()
        if f"class {model}CreateView(CreateView):" in view_file_text:
            print("CreateView already exists")
        else:
            view_file.write_text(
                view_file_text
                + dedent(f"""
            class {model}CreateView(CreateView):
                model = {model}
                template_name = "{model.lower()}s/form.html"
                form_class = {model}CreateForm

                def get_success_url(self) -> str:
                    return reverse("todos:detail", kwargs={{"pk": self.object.pk}})  # type: ignore
            """)
            )
        # detail view
        view_file_text = view_file.read_text()
        if f"class {model}DetailView(DetailView):" in view_file_text:
            print("DetailView already exists")
        else:
            view_file.write_text(
                view_file_text
                + dedent(f"""
            class {model}DetailView(DetailView):
                model = {model}
                template_name = "{model.lower()}s/detail.html"
            """)
            )
        # update view
        view_file_text = view_file.read_text()
        if f"class {model}UpdateView(UpdateView):" in view_file_text:
            print("UpdateView already exists")
        else:
            view_file.write_text(
                view_file_text
                + dedent(f"""
            class {model}UpdateView(UpdateView):
                model = {model}
                template_name = "{model.lower()}s/form.html"
                form_class = {model}UpdateForm

                def get_success_url(self) -> str:
                    return reverse("todos:detail", kwargs={{"pk": self.object.pk}})  # type: ignore
            """)
            )
        # delete view
        view_file_text = view_file.read_text()
        if f"class {model}DeleteView(DeleteView):" in view_file_text:
            print("DeleteView already exists")
        else:
            view_file.write_text(
                view_file_text
                + dedent(f"""
            class {model}DeleteView(DeleteView):
                model = {model}
                template_name = "{model.lower()}s/delete.html"

                def get_success_url(self) -> str:
                    return reverse("todos:list")
            """)
            )

    def create_templates(self, app: str, model: str):
        template_dir = Path(".") / "jinja" / (model.lower() + "s")
        template_dir.mkdir(parents=True, exist_ok=True)

        # base tempalte
        base_template_file = template_dir.parent / "layouts" / (model.lower() + "s.html")
        if not base_template_file.exists():
            base_template_file.write_text((base_template_file.parent / "app.html").read_text())

        # list template
        list_template_file = template_dir / "list.html"
        if list_template_file.exists():
            print("List template already exists")
        else:
            list_template_file.write_text(
                dedent(f"""
                        {{% extends 'layouts/{model.lower()}s.html' %}}

                        {{% block title %}}
                        {model}s
                        {{% endblock title %}}

                        {{% block main %}}
                            {{% for {model.lower()} in {model.lower()}_list %}}
                                {{{{{model.lower()}}}}}
                            {{% endfor %}}
                        {{% endblock main %}}
                        """)
            )
        # form template
        form_template_file = template_dir / "form.html"
        if form_template_file.exists():
            print("Form template already exists")
        else:
            form_template_file.write_text(
                dedent(f"""
                        {{% extends 'layouts/{model.lower()}s.html' %}}

                        {{% set action_url = url("{model.lower()}s:update", pk={model.lower()}.pk) if {model.lower()} else url("{model.lower()}s:create") %}}
                        {{% set cancel_url = url("{model.lower()}s:detail", pk={model.lower()}.pk) if {model.lower()} else url("{model.lower()}s:list") %}}
                        {{% set title = "Update {model}" if {model.lower()} else "Create {model}" %}}

                        {{% block title %}}                        
                            {{{{title}}}}
                        {{% endblock title %}}

                        {{% block main %}} 
                            <form action="{{{{ action_url }}}}" method="post" class="flex flex-col gap-4">
                                {{{{ csrf_input }}}}
                                {{{{ form.as_div() }}}}

                                <div class="flex gap-2">
                                    <a href="{{{{ cancel_url }}}}" class="flex-1 btn">Cancel</a>
                                    <button type="submit" class="flex-1 btn btn-primary">Save</button>
                                </div>
                            </form>
                        {{% endblock main %}}
                        """)
            )

        # detail template
        detail_template_file = template_dir / "detail.html"
        if detail_template_file.exists():
            print("detail template already exists")
        else:
            detail_template_file.write_text(
                dedent(f"""
                        {{% extends 'layouts/{model.lower()}s.html' %}}

                        {{% block title %}}
                        {model} Detail
                        {{% endblock title %}}

                        {{% block main %}}
                            {{{{{model.lower()}}}}}
                        {{% endblock main %}}
                        """)
            )

        # delete template
        delete_template_file = template_dir / "delete.html"
        if delete_template_file.exists():
            print("delete template already exists")
        else:
            delete_template_file.write_text(
                dedent(f"""
                        {{% extends 'layouts/{model.lower()}s.html' %}}

                        {{% block title %}}
                        Delete {model}
                        {{% endblock title %}}

                        {{% block main %}}
                            <form method="post" class="flex flex-col gap-4">
                                {{{{ csrf_input }}}}
                                <div class="prose text-center max-w-none">
                                <h1>Are you sure you want to delete this todo?</h1>
                                </div>

                                <div class="flex gap-2">
                                    <a href="{{{{ url("{model.lower()}s:list") }}}}" class="flex-1 btn">Cancel</a>
                                    <button type="submit" class="flex-1 btn btn-primary">Save</button>
                                </div>
                            </form>
                        {{% endblock main %}}
                        """)
            )
