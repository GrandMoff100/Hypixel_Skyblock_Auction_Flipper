from .utils import get_auctions
from collections import defaultdict


reforges = [
    "Gentle ", "Odd ", "Fast ", "Fair ", "Epic ", "Heroic ", "Sharp ",
    "Spicy ", "Legendary ", "Dirty ", "Fabled ", "Suspicious ", "Withered ",
    "Salty ", "Treacherous ", "Deadly ", "Fine ", "Grand ", "Hasty ", "Neat ",
    "Rapid ", "Unreal ", "Awkward ", "Rich ", "Precise ", "Spiritual ",
    "Clean ", "Fierce ", "Heavy ", "Light ", "Mythic ", "Pure ", "Smart ",
    "Titanic ", "Ancient ", "Necrotic ", "Spiked ", "Renowned ", "Cubic ",
    "Warped ", "Reinforced ", "Loving ", "Ridiculous ", "Giant ", "Bizarre ",
    "Itchy ", "Ominous ", "Pleasant ", "Pretty ", "Shiny ", "Simple ",
    "Strange ", "Vivid ", "Godly ", "Demonic ", "Forceful ", "Hurtful ",
    "Keen ", "Strong ", "Superior ", "Unpleasant ", "Zealous ", "Silky ",
    "Bloody ", "Shaded ", "Sweet ", "Fruitful ", "Magnetic ", "Moil ",
    "Candied ", "Perfect ", "Wise "
]


def bin_auctions(KEY):
    for auction in get_auctions(KEY):
        # This removes pets as well
        if "bin" in auction and "[Lvl " not in auction["item_name"]:
            del (auction["uuid"], auction["auctioneer"], auction["profile_id"],
                 auction["coop"], auction["start"], auction["end"],
                 auction["item_lore"], auction["extra"], auction["bids"],
                 auction["item_bytes"], auction["claimed_bidders"])
        yield auction


SPECIAL_CASES = ["Very ", "Highly ", "Not so ", "Extremely ", "Absolutely ", "Even More "]

def filter_item(auction):
    if "✪✪✪✪" not in auction["item_name"]:
        auction["item_name"] = auction["item_name"].replace("✪", "")
    if any(special_case in auction["item_name"]
           for special_case in SPECIAL_CASES):
        for special_case in SPECIAL_CASES:
            auction["item_name"] = auction["item_name"].replace(
                special_case, "")
    else:
        for reforge in reforges:
            if reforge in auction["item_name"]:
                auction["item_name"] = auction["item_name"].replace(
                    reforge, "")
    return auction["item_name"]


def sorted_by_name(auctions):
    sort = defaultdict(list)
    for auction in auctions:
        name = filter_item(auction)
        if name is not None:
            if auction["item_name"] == name:
                sort[name].append(auction)
    return sort


def get_flips(auctions):
    sort = sorted_by_name(auctions)
    for key in sort:
        cheapest = []
        for item in sort[key]:
            cheapest.append(int(item["starting_bid"]))
        cheapest = sorted(cheapest)[:2]
        if len(cheapest) == 2:
            difference = cheapest[1] * 0.99 - cheapest[0]
            margin = round(difference / cheapest[0] * 100, 1)
            yield {
                "Item Name": key,
                "Buy Price": cheapest[0],
                "Sell Price": cheapest[1] * 0.99,
                "Difference": difference,
                "Profit Margin": margin
            }


def find_profitable_flips(auctions):
    for flip in sorted(get_flips(auctions), key=lambda x: x['Difference']):
        Name = flip["Item Name"]
        Buy = flip["Buy Price"]
        Sell = round(flip["Sell Price"])
        Difference = round(flip["Difference"])
        Profit = flip["Profit Margin"]
        yield {
            "name": Name,
            "buy-price": Buy,
            "sell-price": Sell,
            "profit": Difference,
            "profit-margin": Profit
        }
