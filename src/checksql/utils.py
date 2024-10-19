import html
import polars as pl
from typing import List

def format_column_list(columns: List[str], prefix=None, singular_prefix=None) -> str:
    assert(len(columns) > 0)

    columns = [f'<code>{ html.escape(c) }</code>' for c in columns]

    if prefix:
        if singular_prefix and len(columns) == 1:
            prefix = singular_prefix

        return f'{prefix} { ", ".join(columns) }'
    else:
        return ", ".join(columns)


def normalize_result(df: pl.DataFrame, order_rows=False, order_columns=False) -> pl.DataFrame:
    if order_columns:
        df = df.select(sorted(df.columns))
    if order_rows:
        df = df.sort(df.columns)
    return df

def load_sql(fn) -> str:
    with open(fn, 'r') as fd:
        return fd.read().strip()
