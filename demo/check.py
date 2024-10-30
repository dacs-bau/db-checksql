from pathlib import Path

from checksql.select import SelectQueryChecker as SQC
from checksql.utils import load_sql

DIR = Path(__file__).parent
DBFILE = DIR / 'views.db'

n = '36-ansichten'
CHECKERS = {
    (n, 1): SQC(DBFILE, load_sql(DIR / '1.sql'), check_row_order=False, check_column_order=True),
    (n, 2): SQC(DBFILE, load_sql(DIR / '2.sql'), check_row_order=False, check_column_order=True),
    (n, 3): SQC(DBFILE, load_sql(DIR / '3.sql'), check_row_order=False, check_column_order=True),
    (n, 4): SQC(DBFILE, load_sql(DIR / '4.sql'), check_row_order=False, check_column_order=True),
    (n, 5): SQC(DBFILE, load_sql(DIR / '5.sql'), check_row_order=False, check_column_order=True),
    (n, 6): SQC(DBFILE, load_sql(DIR / '6.sql'), check_row_order=False, check_column_order=True),
    (n, 7): SQC(DBFILE, load_sql(DIR / '7.sql'), check_row_order=True, check_column_order=True),
    (n, 8): SQC(DBFILE, load_sql(DIR / '8.sql'), check_row_order=True, check_column_order=True),
    (n, 9): SQC(DBFILE, load_sql(DIR / '9.sql'), check_row_order=False, check_column_order=True)
}

def get_checkers():
    for name, check in CHECKERS.items():
        yield name[0], name[1], check