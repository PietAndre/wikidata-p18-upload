import csv
import os
from wikibaseintegrator import WikibaseIntegrator
from wikibaseintegrator.datatypes import CommonsMedia
from wikibaseintegrator.wbi_enums import ActionIfExists

user = os.getenv("WIKIDATA_USER")
token = os.getenv("WIKIDATA_TOKEN")

wbi = WikibaseIntegrator(user=user, token=token)

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
