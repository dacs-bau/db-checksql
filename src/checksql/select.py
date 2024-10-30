import html
import apsw
import apsw.ext
import polars as pl



from .findings import Findings
from .exceptions import CheckAbortedException
from .utils import format_column_list, normalize_result


class SelectQueryChecker:
    def __init__(self, dbfile, query, check_row_order=False, check_column_order=False):
        self._dbfile = dbfile
        self._query = query
        self._check_row_order = check_row_order
        self._check_column_order = check_column_order

        expected = self.execute_query(self._query)
        self._results = normalize_result(expected, not check_row_order, not check_column_order)

    def execute_query(self, query: str, findings=Findings(), row_limit: int = 100000) -> pl.DataFrame:
        with apsw.Connection(str(self._dbfile), flags=apsw.SQLITE_OPEN_READONLY, statementcachesize=0) as db:
            db.config(apsw.SQLITE_DBCONFIG_DQS_DML, 0)
            db.config(apsw.SQLITE_DBCONFIG_DQS_DDL, 0)
            db.limit(apsw.SQLITE_LIMIT_ATTACHED, 0)
            db.pragma("foreign_keys", "ON")

            try:
                query_info = apsw.ext.query_info(db, query)
            except apsw.SQLError as ex:
                findings.error(f'Datenbankfehler: <code>{html.escape(str(ex))}</code>.')
                raise CheckAbortedException()

            if not query_info.is_readonly:
                findings.exploit("Ihre Anfrage soll keine Daten einfügen, löschen oder verändern.")
                raise CheckAbortedException()

            if query_info.query_remaining is not None:
                findings.error(f"""
                  <p>
                  Ihre Lösung besteht aus mehreren Abfragen.
                  Bitte Lösen Sie die Aufgabe mit einer einzigen Abfrage.
                  </p>
                  <details>
                    <summary>Erste Abfrage</summary>
                    <pre><code>{ html.escape(query_info.first_query).strip() }</code></pre>
                  </details>
                  <details>
                    <summary>Restliche(n) Abfrage(n)</summary>
                    <pre><code>{ html.escape(query_info.query_remaining).strip() }</code></pre>
                  </details>
                """)
                raise CheckAbortedException()

            # Check for duplicate column names
            column_names = []
            duplicate_column_names = set()
            for c in query_info.description:
                name = c[0]
                if name in column_names:
                    duplicate_column_names.add(name)
                    while name in column_names:
                        name += "_"
                column_names.append(name)

            for name in duplicate_column_names:
                findings.warning(f'Das Abfrageergebnis enthält mehrere Spalten mit dem Namen <code>{ html.escape(name) }</code>.')

            cursor = db.cursor()
            raw_results = []
            try:
                for row in cursor.execute(query):
                    raw_results.append(row)
                    if len(raw_results) > row_limit:
                        findings.error('Die Ausführung der Abfrage wurde abgebrochen, da das Ergebnis viel zu viele Zeilen enthält.')
                        raise CheckAbortedException()
            except apsw.SQLError as ex:
                findings.error(f'Datenbankfehler: <code>{ html.escape(str(ex)) }</code>.')
                raise CheckAbortedException

            return pl.DataFrame(raw_results, schema=column_names, orient='row')

    def check_result(self, query: str, findings: Findings):
        observed = self.execute_query(query, findings=findings, row_limit=len(self._results) * 5)
        observed = normalize_result(observed, not self._check_row_order, not self._check_column_order)

        expected = self._results
        if observed.columns != expected.columns:
            if sorted(observed.columns) == sorted(expected.columns):
                wrong_column_order = True
                o = format_column_list(observed.columns, "")
                e = format_column_list(expected.columns, "")
                findings.error(f"Reihenfolge der Spalten falsch. Erwartet wird die Reihenfolge { e }, die Abfrage liefert allerdings die Reihenfolge { o }.")
            else:
                missing_columns = list(set(expected.columns) - set(observed.columns))
                unexpected_columns = list(set(observed.columns) - set(expected.columns))

                if len(missing_columns) > 0:
                    m = format_column_list(missing_columns,
                                           "<em>fehlen</em> die Spalten",
                                           "<em>fehlt</em> die Spalte")
                    findings.error(f"Es {m} im Abfrageergebnis.")

                if len(unexpected_columns) > 0:
                    m = format_column_list(unexpected_columns,
                                           "<em>überflüssigen</em> Spalten",
                                           "<em>überflüssige</em> Spalte")
                    findings.warning(f"Ergebnis enthält die { m }.")
            raise CheckAbortedException()

        if not observed.equals(expected):
            ## FIXME: Lustigere Fehlersprüche einbauen.
            findings.error("Das Ergebnis der Abfrage entspricht <strong>nicht</strong> dem erwarteten Ergebnis.")

    def __call__(self, query: str, findings=Findings()):
        self.check_result(query, findings)
