import json
import logging
from dataclasses import dataclass

from fastapi import FastAPI

import requests
import bs4

app = FastAPI()

STATUS_MAP = {
    "ags-ServerStatus-content-responses-response-server-status--full": "full",
    "ags-ServerStatus-content-responses-response-server-status--up": "up"
}

r = requests.get("https://www.newworld.com/en-us/support/server-status")
soup = bs4.BeautifulSoup(r.text, "html.parser")


@dataclass
class ServerInfo:
    server_name: str
    status: str


def get_server_status_from_response_div(server) -> ServerInfo:
    status_div = server.find(
        "div", attrs={"class": "ags-ServerStatus-content-responses-response-server-status-wrapper"}
    ).find("div", attrs="ags-ServerStatus-content-responses-response-server-status")
    server_name_div = server.find("div", attrs={"class": "ags-ServerStatus-content-responses-response-server-name"})
    server_name = server_name_div.text.strip()
    status_class = status_div.attrs["class"][1]
    return ServerInfo(
        server_name=server_name,
        status=STATUS_MAP.get(status_class, "down")
    )


def get_regions(website_response) -> dict:
    divs = website_response.find_all("a", attrs={"class": "ags-ServerStatus-content-tabs-tabHeading"})
    region_map = {}
    for div in divs:
        region_map[div.attrs["data-index"]] = div.find("div").text.strip()
    return region_map


def get_server_statuses_for_region(region_soup) -> dict:
    servers = region_soup.find_all("div", attrs={"class": "ags-ServerStatus-content-responses-response-server"})
    server_status = {}
    for server in servers:
        server_info = get_server_status_from_response_div(server)
        if server_info.server_name in server_status:
            logging.warning(f"duplicate server name {server_info.server_name}")
        server_status[server_info.server_name] = server_info.status
    return server_status


@app.get("/")
async def main():
    region_map = get_regions(soup)
    full_response = {}
    for data_index, region_name in region_map.items():
        region_div = soup.find(
            "div", attrs={"class": "ags-ServerStatus-content-responses-response", "data-index": data_index}
        )
        server_statuses = get_server_statuses_for_region(region_div)
        full_response[region_name] = server_statuses
    return full_response


if __name__ == "__main__":
    main()
