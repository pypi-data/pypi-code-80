from typing import Optional

from hltb_oracle.models import HowLongToBeatPage
from hltb_oracle.parser import HowLongToBeatParser
from hltb_oracle.website import HowLongToBeatWebsite, SortBy


class HowLongToBeatOracle:
    @staticmethod
    def get(
        search_query: Optional[str] = None,
        page: Optional[int] = None,
        sort_by: SortBy = SortBy.most_popular,
        only_recently_updated=False,
    ):
        query_string = "recently updated" if only_recently_updated else search_query
        html = HowLongToBeatWebsite.search_results(
            query_string=query_string,
            page=page,
            sort_by=sort_by,
        )
        result = HowLongToBeatParser.parse_game_list(html)
        return HowLongToBeatPage(result)
