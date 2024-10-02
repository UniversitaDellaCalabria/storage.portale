from functools import reduce
import operator
from django.db.models import Q


class ServiceQueryBuilder:
    @staticmethod
    def build_filter_chain(params_dict, query_params, *args):
        return reduce(
            operator.and_,
            [
                Q(**{v: query_params.get(k)})
                for (k, v) in params_dict.items()
                if query_params.get(k)
            ]
            + list(args),
            Q(),
        )
