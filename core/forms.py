from django import forms


class BaseForm(forms.Form):
    error_css_class = "is-invalid"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields[field_name]

            # add form-control class to all fields
            current_class = field.widget.attrs.get("class", "")
            current_class = f"{current_class} form-control"

            # add error class
            if field_name in self.errors:
                current_class = f"{current_class} is-invalid"

            # add blank placeholder to all fields
            # this is needed for bootstrap floating labels
            current_placeholder = field.widget.attrs.get("placeholder", "")

            # apply the new class
            field.widget.attrs["class"] = current_class
            # applyt the new placeholder
            field.widget.attrs["placeholder"] = current_placeholder
