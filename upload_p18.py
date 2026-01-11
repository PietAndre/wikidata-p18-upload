import csv
import os
from wikibaseintegrator import WikibaseIntegrator
from wikibaseintegrator.datatypes import CommonsMedia, URL, Time
from wikibaseintegrator.wbi_enums import ActionIfExists
from wikibaseintegrator.wbi_login import Login

# Login met OAuth1 (nieuwe API)
login = Login(
    consumer_key=os.getenv("WIKIDATA_CONSUMER_KEY"),
    consumer_secret=os.getenv("WIKIDATA_CONSUMER_SECRET")
)

wbi = WikibaseIntegrator(login=login)

# CSV bestand
csv_file = "P18-CRACO-QID-GithubQuickstatements.csv"

with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        qid = row["QID"].strip()
        filename = row["P18"].strip()

        # Ophalen item
        item = wbi.item.get(entity_id=qid)

        # P18 claim toevoegen
        claim = CommonsMedia(
            prop_nr="P18",
            value=filename,
            action_if_exists=ActionIfExists.REPLACE
        )

        # Reference URL toevoegen (P854)
        ref_url = URL(
            prop_nr="P854",
            value=f"https://commons.wikimedia.org/wiki/File:{filename}"
        )

        # Retrieved datum (P813)
        ref_date = Time(
            prop_nr="P813",
            time="+2026-01-11T00:00:00Z"
        )

        claim.add_reference([ref_url, ref_date])

        item.claims.add(claim)
        item.write(summary="Add image (P18) with reference and retrieved date")
        print(f"✔ {qid} → {filename}")
