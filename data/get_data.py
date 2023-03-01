#! /usr/bin/env python3

import requests
import os
import sys
import pandas as pd


def parse_card(card_info):
    parsed = {}
    parsed["id"] = card_info["id"]
    parsed["name"] = card_info["name"]
    parsed["type"] = card_info["type"]
    parsed["frame"] = card_info["frameType"]
    parsed["card_text"] = card_info["desc"]
    parsed["tcgplayer_price_usd"] = card_info["card_prices"][0]["tcgplayer_price"]
    parsed["cardmarket_price_eur"] = card_info["card_prices"][0]["cardmarket_price"]
    parsed["num_alternative_arts"] = (
        len(card_info["card_images"]) - 1
    )  # One of the card images is the original
    parsed["image_url"] = card_info["card_images"][0]["image_url"]

    if "card_sets" in card_info:
        parsed["num_reprints"] = (
            len(card_info["card_sets"]) - 1
        )  # One of the prints is not a reprint

    if "archetype" in card_info:
        parsed["archetype"] = card_info["archetype"]

    if "monster" in parsed["type"].lower():
        parsed["atk"] = card_info["atk"]
        parsed["level"] = (
            card_info["level"] if "level" in card_info else card_info["linkval"]
        )
        parsed["attribute"] = card_info["attribute"]
        parsed["monster_type"] = card_info["race"]

        if "pendulum" in parsed["type"].lower():
            parsed["scale"] = card_info["scale"]

        if "link" in parsed["type"].lower():
            parsed["link_markers"] = card_info["linkmarkers"]
        else:
            parsed["def"] = card_info["def"]

    elif "spell" in parsed["type"].lower():
        parsed["spell_type"] = card_info["race"]

    elif "trap" in parsed["type"].lower():
        parsed["trap_type"] = card_info["race"]

    return parsed


def main():

    url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

    response = requests.get(url)

    if response.status_code != 200:
        sys.exit("Could not fetch card data")

    data = response.json()["data"]

    parsed_data = [parse_card(card) for card in data]

    df = pd.DataFrame(parsed_data)
    df = df.set_index("id")
    df = df[
        [
            "name",
            "type",
            "archetype",
            "tcgplayer_price_usd",
            "cardmarket_price_eur",
            "num_reprints",
            "num_alternative_arts",
            "monster_type",
            "spell_type",
            "trap_type",
            "atk",
            "def",
            "level",
            "attribute",
            "scale",
            "link_markers",
            "frame",
            "image_url",
            "card_text",
        ]
    ]
    df.to_csv(os.path.join("data", "cards.csv"))


if __name__ == "__main__":
    main()
