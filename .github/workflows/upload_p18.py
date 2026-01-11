import csv
import os
from wikibaseintegrator import WikibaseIntegrator
from wikibaseintegrator.models.claim import Claim
from wikibaseintegrator.datatypes import Time

# OAuth setup
wbi = WikibaseIntegrator(
    user=os.getenv("WIKIDATA_USER"),
    token=os.getenv("WIKIDATA_TOKEN"),
    mediawiki_api_url="https://www.wikidata.org/w/api.php"
)

with open("images.csv", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        qid = row['qid']
        filename = row['filename']
        reference_url = row.get('reference_url')

        # Maak P18 claim
        claim = Claim(prop_nr="P18", value=filename)

        # Voeg reference toe
        if reference_url:
            claim.add_reference([
                Claim(prop_nr="S854", value=reference_url),
                Claim(prop_nr="S813", value=Time(year=2026, month=1, day=11))
            ])

        # Haal item op en voeg claim toe
        wbi_item = wbi.item.get(qid)
        wbi_item.add_claims([claim])
        wbi_item.write()
        print(f"{qid} updated with {filename}")
