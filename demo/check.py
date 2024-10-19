from pathlib import Path

from checksql.select import SelectQueryChecker
from checksql.utils import load_sql

DIR = Path(__file__).parent
DBFILE = DIR / 'views.db'

def register_checkers(checkers):
    n = '36-ansichten'
    checkers[(n, 1)] = SelectQueryChecker(DBFILE, load_sql(DIR / '1.sql'), check_row_order=False, check_column_order=True)
    checkers[(n, 2)] = SelectQueryChecker(DBFILE, load_sql(DIR / '2.sql'), check_row_order=False, check_column_order=True)
    checkers[(n, 3)] = SelectQueryChecker(DBFILE, load_sql(DIR / '3.sql'), check_row_order=False, check_column_order=True)
    checkers[(n, 4)] = SelectQueryChecker(DBFILE, load_sql(DIR / '4.sql'), check_row_order=False, check_column_order=True)
    checkers[(n, 5)] = SelectQueryChecker(DBFILE, load_sql(DIR / '5.sql'), check_row_order=False, check_column_order=True)
    checkers[(n, 6)] = SelectQueryChecker(DBFILE, load_sql(DIR / '6.sql'), check_row_order=False, check_column_order=True)
    checkers[(n, 7)] = SelectQueryChecker(DBFILE, load_sql(DIR / '7.sql'), check_row_order=True, check_column_order=True)
    checkers[(n, 8)] = SelectQueryChecker(DBFILE, load_sql(DIR / '8.sql'), check_row_order=True, check_column_order=True)
    checkers[(n, 9)] = SelectQueryChecker(DBFILE, load_sql(DIR / '9.sql'), check_row_order=False, check_column_order=True)
