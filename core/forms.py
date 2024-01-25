from django import forms


class BaseForm(forms.Form):
    error_css_class = "is-invalid"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields[field_name]

            # add form-control class to all fields
            current_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{current_class} form-control"

            # add blank placeholder to all fields
            # this is needed for bootstrap floating labels
            current_placeholder = field.widget.attrs.get("placeholder", "")
            if not current_placeholder:
                field.widget.attrs["placeholder"] = ""
