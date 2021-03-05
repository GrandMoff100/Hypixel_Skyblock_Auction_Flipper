import requests as r
import json


HYPIXEL_API = "https://api.hypixel.net/"

with open('key.json') as f:
    keys = json.load(f)["keys"]


def get_key():
    i = 0
    while True:
        yield keys[i % len(keys)]
        i += 1

def get_auctions(key):
    response = r.get(HYPIXEL_API + "skyblock/auctions" + f"?key={key}").json()

    if "error" in response:
        raise MemoryError(response['error'], response['cause'])

    auctions = response['auctions']
    page_count = response['totalPages']

    print('Total Pages:', page_count)
    print('Total Auctions:', response['totalAuctions'])
    
    yield from auctions
    for i in range(1, page_count):
        print('Getting Page:', f'{i}/{page_count}')
        page = r.get(HYPIXEL_API + "skyblock/auctions" + f"?key={key}&page={i}")

        try:
            page = page.json()
        except json.decoder.JSONDecodeError:
            print(page.content[:500])

        if "error" in page:
            raise MemoryError(page['error'], page['cause'])
        try:
            yield from page['auctions']
        except KeyError:
            print(page.keys())
    
    print('Getting Page:', f'{i+1}/{page_count}')
    print('Finished Getting Pages.')

