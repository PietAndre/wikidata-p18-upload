import csv
import os
from wikibaseintegrator import WikibaseIntegrator
from wikibaseintegrator.datatypes import CommonsMedia
from wikibaseintegrator.wbi_enums import ActionIfExists
from wikibaseintegrator.wbi_login import OAuth1

login = OAuth1(
    consumer_key=os.getenv("WIKIDATA_CONSUMER_KEY"),
    consumer_secret=os.getenv("WIKIDATA_CONSUMER_SECRET")
)

wbi = WikibaseIntegrator(login=login)

csv_file = "P18-CRACO-QID-GithubQuickstatements.csv"

with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        qid = row["QID"].strip()
        filename = row["P18"].strip()

        item = wbi.item.get(entity_id=qid)

        item.claims.add(
            CommonsMedia(
                prop_nr="P18",
                value=filename,
                action_if_exists=ActionIfExists.REPLACE
            )
        )

        item.write(summary="Add image (P18) from Wikimedia Commons")
        print(f"✔ {qid} → {filename}")
