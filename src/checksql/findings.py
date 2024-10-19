class Findings:
    def __init__(self):
        self._findings = []

    def __len__(self):
        return len(self._findings)
    
    def __getitem__(self, i):
        return self._findings[i]
    
    def _add_message(self, type, message):
        self._findings.append({"type": type, "message": message})

    def correct(self, message):
        self._add_message("correct", message)
    
    def funny(self, message):
        self._add_message("funny", message)
    
    def info(self, message):
        self._add_message("info", message)

    def warning(self, message):
        self._add_message("warning", message)

    def error(self, message):
        self._add_message("error", message)

    def syserror(self, message):
        self._add_message("syserror", message)

    def exploit(self, message):
        message = f"""<p>{message}</p>
<details open>
<summary>Hinweis für Hacker und Haecksen</summary>
Sie können den SQL-Checker gerne pentesten.
Gerne richten wir Ihnen einen Zugang zu einem dedizierten API-Server ein, so stören Sie nicht den Produktivbetrieb.
Danke!
</details>
"""
        self._add_message("exploit", message)

    def to_list(self) -> list:
        return self._findings.copy()