import html
import random

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .findings import Findings
from .exceptions import CheckAbortedException

# Liste mit Gratulationen wenn alles richtig ist.
GOOD_JOB = [
    "Bäm! So löst man die Aufgabe!",
    "Herzlichen Glückwunsch, E. F. Codd wäre stolz auf Sie!",
    "Die Aufgabe haben Sie gerockt. Weiter so!",
    "Respekt, Sie haben die Aufgabe wie ein echter Datenbank-Ninja gelöst!",
    "Genial! Ihre SQL-Query ist ein Datenbanktraum!",
    "Wow! Diese Abfrage ist präziser als ein Schweizer Uhrwerk!",
    "Donnerwetter! Diese Query würde selbst Larry Ellison beeindrucken!",
    "Grandios! Mit diesem SELECT haben Sie den Jackpot geknackt!",
    "Fantastisch! Ihre SQL-Syntax glänzt wie ein Diamant!",
    "Beeindruckend! Diese Abfrage ist ordnungsgemäßer als ein Verwaltungshandbuch!",
    "Mustergültig! Ihre SQL-Kenntnis verdient eine Beförderung in die nächste Besoldungsgruppe!",
    "Formvollendet! Ihre Query ist so korrekt wie ein perfekt ausgefülltes Antragsformular!",
    "Erstklassig! Ihre SQL-Fähigkeiten sind so verlässlich wie ein Beamter auf Lebenszeit!",
    "Hochoffiziell bestätigt: Ihre Abfrage erfüllt alle Kriterien der Datenbankabfrageverordnung!",
]

CHECKERS = {}

ORIGINS = [
    "http://127.0.0.1:8080",
    "https://db-ws2024.dacsbund.de",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/health-check")
async def healthCheck() -> str:
    return "OK"


@app.get("/api/v1/known-checks")
async def knownChecks() -> list:
    """Get a list of all known checks"""
    return list(CHECKERS.keys())


@app.get("/api/v1/check-answer")
async def checkAnswer(pset: str, pid: int, query: str) -> list:
    findings = Findings()

    if len(query.strip()) == 0:
        findings.funny("Keine Antwort ist auch keine Lösung.")
        return findings.to_list()

    try:
        CHECKERS[(pset, pid)](query, findings=findings)
    except MemoryError:
        findings.exploit("Speicherverbrauch beim ausführen der Abfrage zu hoch. Ihre Abfrage liefert zu viele Zeilen zurück.")
    except KeyError:
        findings.syserror(f"Unbekannte Aufgabe <code>{ html.escape(pset) }</code> <code>{ html.escape(pid) }</code>.")
    except CheckAbortedException:
        if len(findings) == 1:
            findings.info("Prüfung wegen des obigen Fehlers frühzeitig abgebrochen. Bitte korrigieren Sie den Fehler damit alle Tests durchlaufen können.")
        else:
            findings.info("Prüfung wegen der obigen Fehler frühzeitig abgebrochen. Bitte korrigieren Sie die Fehler damit alle Tests durchlaufen können.")

    if len(findings) == 0:
        findings.correct(random.choice(GOOD_JOB))

    return findings.to_list()
