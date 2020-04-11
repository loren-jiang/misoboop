from django import forms

class CachingModelChoicesFormSet(forms.BaseInlineFormSet):
    """
    Used to avoid duplicate DB queries by caching choices and passing them all the forms.
    To be used in conjunction with `CachingModelChoicesForm`.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form = self._construct_form(0)
        self.cached_choices = {}
        try:
            model_choice_fields = form.model_choice_fields
        except AttributeError:
            pass
        else:
            for field_name in model_choice_fields:
                if field_name in form.fields and not isinstance(
                    form.fields[field_name].widget, forms.HiddenInput):
                    self.cached_choices[field_name] = list(form.fields[field_name].choices)

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['cached_choices'] = self.cached_choices
        return kwargs


class CachingModelChoicesForm(forms.ModelForm):
    """
    Gets cached choices from `CachingModelChoicesFormSet` and uses them in model choice fields in order to reduce
    number of DB queries when used in admin inlines.
    """

    @property
    def model_choice_fields(self):
        return [fn for fn, f in self.fields.items()
            if isinstance(f, (forms.ModelChoiceField, forms.ModelMultipleChoiceField,))]

    def __init__(self, *args, **kwargs):
        cached_choices = kwargs.pop('cached_choices', {})
        super().__init__(*args, **kwargs)
        for field_name, choices in cached_choices.items():
            if field_name in self.fields and len(choices):
                self.fields[field_name].choices = choices
