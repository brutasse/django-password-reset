from django import forms


class PlaceholderForm(object):
    def set_placeholder(self):
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                if isinstance(field.widget, forms.TextInput) or isinstance(field.widget, forms.EmailInput):
                    widget_attrs = field.widget.attrs.copy()
                    widget_attrs.update({'placeholder': field.label})
                    field.widget = field.widget.__class__(attrs=widget_attrs)
