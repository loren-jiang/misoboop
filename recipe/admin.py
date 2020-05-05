from django.contrib import admin

from .models import Recipe, Ingredient, Direction, IngredientAmount, Unit
from core.forms import CachingModelChoicesFormSet, CachingModelChoicesForm
from django import forms
from django.urls import resolve
from adminsortable.admin import NonSortableParentAdmin, SortableTabularInline, SortableStackedInline
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from .forms import DirectionForm
from tinymce.widgets import TinyMCE

# Register your models here.

class IngredientAmountInlineForm(forms.ModelForm):
    def clean_unit(self):
        unit = self.cleaned_data.get('unit', None)
        if unit is None:
            raise forms.ValidationError("Please add unit.")
        return unit

    # def clean(self):
    #     cleaned_data = super().clean()

    class Meta:
        model = IngredientAmount
        exclude = ()


class CachingIngredientAmountInlineForm(CachingModelChoicesForm, IngredientAmountInlineForm):
    class Meta(IngredientAmountInlineForm.Meta):
        pass

class DirectionInlineForm(CachingModelChoicesForm):
    class Meta:
        model = Direction
        exclude = ()


class DirectionInline(SortableTabularInline):
    model = Direction
    form = DirectionInlineForm
    formset = CachingModelChoicesFormSet
    extra = 1
    # raw_id_fields = ("ingredient_amounts",)

    def get_parent_object_from_request(self, request):
        """
        Returns the parent object from the request or None.

        Note that this only works for Inlines, because the `parent_model`
        is not available in the regular admin.ModelAdmin as an attribute.
        """
        resolved = resolve(request.path_info)
        obj_id = resolved.kwargs.get('object_id')
        if obj_id:
            return self.parent_model.objects.get(pk=obj_id)
        return None

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "ingredient_amounts":
            kwargs["queryset"] = IngredientAmount.objects.filter(recipe=self.get_parent_object_from_request(request))
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('recipe').prefetch_related('ingredient_amounts')

class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount

    autocomplete_fields = ['ingredient']
    form = IngredientAmountInlineForm
    # formset = CachingModelChoicesFormSet
    extra = 3

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('ingredient', 'recipe', 'unit')

class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    search_fields = ['name']

class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class RecipeNameFilter(InputFilter):
    parameter_name = 'name'
    title = _('Name')

    def queryset(self, request, queryset):
        if self.value():
            input_text = self.value()
            return queryset.filter(Q(name__icontains=input_text))

class RecipeTagsFilter(InputFilter):
    parameter_name = 'tags'
    title = _('Tag')

    def queryset(self, request, queryset):
        if self.value():
            input_tag = self.value()
            return queryset.filter(Q(tags__name__in=[input_tag]))

class RecipeAdmin(NonSortableParentAdmin):
    inlines = (
        IngredientAmountInline,
        DirectionInline,
    )
    list_filter = (RecipeNameFilter, RecipeTagsFilter)
    list_display = ('name', 'recipe_tags',)


    def get_queryset(self, request):
        return Recipe.objects.get_all()

    def recipe_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.order_by()])

    # search_fields = ['name', 'author__username']

class DirectionAdmin(admin.ModelAdmin):
    model = Direction
    form = DirectionForm



admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Direction, DirectionAdmin)
admin.site.register(Unit)
