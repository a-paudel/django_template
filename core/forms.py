from django import forms


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields[field_name]

            # add form-control class to all fields
            current_class = field.widget.attrs.get("class", "")
            current_class = f"{current_class} input"

            # add error class
            if field_name in self.errors:
                current_class = f"{current_class} border-red-6"

            # apply the new class
            field.widget.attrs["class"] = current_class
