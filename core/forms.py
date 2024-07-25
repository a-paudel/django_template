from django import forms
from django.utils.safestring import SafeText
from django.template.loader import render_to_string


class BaseForm(forms.Form):
    error_css_class = "text-error"

    def as_div(self):
        # render the components/form.html template with the form
        html = render_to_string("components/form.html", {"form": self})
        return SafeText(html)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            new_classes = ""

            is_checkbox = isinstance(field.widget, forms.CheckboxInput)
            is_radio = isinstance(field.widget, forms.RadioSelect)
            is_select = isinstance(field.widget, forms.Select)
            is_textarea = isinstance(field.widget, forms.Textarea)

            # add input and input-bordered classes to all fields
            # except if it is a checkbox or radio, these have different classes
            if is_checkbox:
                new_classes += "toggle toggle-success"
            elif is_radio:
                new_classes += "radio"
            else:
                new_classes += "input input-bordered w-full"

            has_error = self.errors.get(field_name)
            # if the field has errors, add the input-error class (except checkbox and radio)
            if not is_checkbox and not is_radio and has_error:
                new_classes += " input-error"

            # replace the class name for each type
            if is_select:
                # select-bordered select-error
                new_classes = new_classes.replace("input", "select")
            elif is_textarea:
                # textarea-bordered textarea-error
                new_classes = new_classes.replace("input", "textarea")

            initial_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{initial_classes} {new_classes}"
