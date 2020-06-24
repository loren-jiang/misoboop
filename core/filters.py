from rest_framework.filters import OrderingFilter
import django_filters
from django.db.models import Q, F
from functools import reduce
import operator
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

class NullsAlwaysLastOrderingFilter(OrderingFilter):
    """ Use Django nulls_last feature to force nulls to bottom in all orderings. """

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        print(ordering)
        if ordering:
            f_ordering = []
            for o in ordering:
                # if not o:
                #     continue
                if o[0] == '-':
                    f_ordering.append(F(o[1:]).desc(nulls_last=True))
                else:
                    f_ordering.append(F(o).asc(nulls_last=True))

            return queryset.order_by(*f_ordering)
        return queryset


class IcontainsInFilter(django_filters.Filter):
    def __init__(self, *args, **kwargs):
        self.query_param = kwargs.pop('query_param', None)
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        params = list(filter(
            lambda x: x,  # filters empty strings
            self.parent.request.GET.getlist(self.query_param, [])))
        if params:
            clauses = (Q(**{self.lookup_expr: ing}) for ing in params)
            query = reduce(operator.or_, clauses)
            qs = qs.filter(query).distinct()
        return qs

class SearchFilter(django_filters.Filter):
    def __init__(self, lookups, weights=None, *args, **kwargs):
        self.lookups = lookups
        # self.weights = weights
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        # todo: implement more robust search ranking w/ weights
        search_vector = SearchVector(*self.lookups)
        search_query = SearchQuery(value)
        # search_rank = SearchRank(search_vector, search_query, weights=self.weights)

        if value and self.lookups:
            qs = qs.annotate(search=search_vector).filter(search=search_query)
            # qs = qs.annotate(rank=search_rank).order_by('-rank')
        return qs
