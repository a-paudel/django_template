from django import forms


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field = self.fields[field_name]

            is_checkbox = isinstance(field.widget, forms.CheckboxInput)
            is_radio = isinstance(field.widget, forms.RadioSelect)
            is_textarea = isinstance(field.widget, forms.Textarea)

            current_class = field.widget.attrs.get("class", "")

            if is_checkbox:
                current_class += "toggle"
            elif is_radio:
                current_class += "radio"
            elif is_textarea:
                current_class += "textarea textarea-bordered"
            else:
                current_class += "input input-bordered"

            if field.error_messages:
                if is_checkbox or is_radio:
                    continue
                elif is_textarea:
                    current_class += " textarea-error"
                else:
                    current_class += " input-error"

            field.widget.attrs["class"] = current_class
