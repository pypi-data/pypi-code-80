# -*- coding: utf-8 -*-
"""
This plugin extends the original series plugin
by FELD Boris <lothiraldan@gmail.com>
Copyright (c) Leonardo Giordani <giordani.leonardo@gmail.com>
Joins articles in a series and provides variables to
manage the series in the template.
"""

from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from operator import attrgetter
from typing import Dict, List, Optional

from pelican.contents import Article
from pelican.generators import ArticlesGenerator

from pelican import signals


@dataclass
class SeriesArticle:
    index: Optional[int]
    date: date
    article: Article


def _sort_articles(series_articles: List[SeriesArticle]) -> List[Article]:
    # This is not DRY but very simple to understand
    forced_order_articles = [
        article for article in series_articles if article.index is not None
    ]

    date_order_articles = [
        article for article in series_articles if article.date is None
    ]

    forced_order_articles.sort(key=attrgetter("index"))
    date_order_articles.sort(key=attrgetter("date"))

    all_articles = forced_order_articles + date_order_articles
    return [article.article for article in all_articles]


def aggregate_series(generator: ArticlesGenerator) -> None:
    series: Dict[str, List[SeriesArticle]] = defaultdict(list)

    # This cycles through all articles in the given generator
    # and collects the 'series' metadata, if present.
    # The 'series_index' metadata is also stored, if specified
    for article in generator.articles:
        if "series" in article.metadata:
            series[article.metadata["series"]].append(
                SeriesArticle(
                    article.metadata.get("series_index", None),
                    article.metadata["date"],
                    article,
                )
            )

    # This uses items() which on Python2 is not a generator
    # but we are dealing with a small amount of data so
    # there shouldn't be performance issues =)
    for series_name, series_articles in series.items():
        ordered_articles = _sort_articles(series_articles)

        for index, article in enumerate(ordered_articles):
            article.series = {
                "name": series_name,
                "index": index + 1,
                "all": ordered_articles,
                "all_previous": ordered_articles[0:index],
                "all_next": ordered_articles[index + 1 :],
                "previous": ordered_articles[index - 1] if index > 0 else None,
                "first": ordered_articles[0],
                "last": ordered_articles[-1],
            }

            try:
                article.series["next"] = ordered_articles[index + 1]
            except IndexError:
                article.series["next"] = None


def register():
    signals.article_generator_finalized.connect(aggregate_series)
