import requests
from bs4 import BeautifulSoup
import json
import sys

session = requests.Session()

base_url = "https://www.openbugbounty.org"
items_per_page = 50


def fetch_page(page):
    results = []
    r = session.post(
        base_url + "/bugbounty-list/ajax.php",
        data={"start": page * items_per_page},
        allow_redirects=False
    )
    if r.status_code != 200:
        return False

    items = json.loads(r.text)
    for item in items['data']:
        results += process_item(item[0].split('"')[1])

    return results


def process_item(program):
    target = base_url + program
    r = session.get(target)
    s = BeautifulSoup(r.text, 'lxml')
    bounty_table = s.find('table', {'class': 'open-bounty'})
    p = bounty_table.find_all('td')
    return map(lambda x: x.text, p)


def store_domain_list(out_file, domains):
    with open(out_file, 'w') as f:
        for d in domains:
            f.write(prepare(d) + '\n')


def prepare(domain):
    if domain.startswith("*."):
        return domain[2:]
    else:
        return domain


def main():
    out_file = 'openbountyprogram_domains.txt'
    if len(sys.argv) > 1:
        out_file = sys.argv[1]

    results = []
    for i in range(0, 100):
        result = fetch_page(i)

        if not result:
            break

        results += result

    store_domain_list(out_file, results)


if __name__ == "__main__":
    main()
