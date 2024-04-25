import requests
import re

from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_build(session):
    build_num = 287665 #fallback value incase function fails
    release_hash = "c843e820d559e1442507cb1fc1f89517be35d345" #fallback value incase function fails

    request = session.get(
        "https://discord.com/login",
        headers = {"Accept-Encoding": "identity"}
    )

    if request.status_code != 200:
        print("Failed to fetch the page. Resorting to default values.")
        return build_num, release_hash

    soup = BeautifulSoup(request.text, "html.parser")
    urls = []

    for script in soup.find_all("script"):
        src = script.get("src")

        if src:
            full_url = urljoin("https://discord.com/login", src)
            urls.append(full_url)

    for url in urls:
        build_request = session.get(
            url,
            headers = {"Accept-Encoding": "identity"}
        )

        if build_request.status_code != 200:
            continue

        build_nums = re.findall(r'buildNumber\D+(\d+)', build_request.text)
        release_hashes = re.findall(r'release:"discord_web-([a-f0-9]+)"', build_request.text)

        if build_nums and release_hashes:
            return build_nums[0], release_hashes[0]

    print("Failed to fetch Build Number and Release Hash, resorting to default values.")

    return build_num, release_hash

build, hash = fetch_build(requests.Session())
