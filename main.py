from utils import get_auctions, get_key()

reforges = [
    "Gentle ", 
    "Odd ", 
    "Fast ", 
    "Fair ", 
    "Epic ", 
    "Heroic ", 
    "Sharp ", 
    "Spicy ", 
    "Legendary ", 
    "Dirty ", 
    "Fabled ", 
    "Suspicious ", 
    "Withered ", 
    "Salty ", 
    "Treacherous ", 
    "Deadly ", 
    "Fine ", 
    "Grand ", 
    "Hasty ", 
    "Neat ", 
    "Rapid ", 
    "Unreal ", 
    "Awkward ", 
    "Rich ", 
    "Precise ",
    "Spiritual ",
    "Clean ",
    "Fierce ",
    "Heavy ",
    "Light ",
    "Mythic ",
    "Pure ",
    "Smart ",
    "Titanic ",
    "Ancient ",
    "Necrotic ",
    "Spiked ",
    "Renowned ",
    "Cubic ",
    "Warped ",
    "Reinforced ",
    "Loving ",
    "Ridiculous ",
    "Giant ",
    "Bizarre ",
    "Itchy ",
    "Ominous ",
    "Pleasant ",
    "Pretty ",
    "Shiny ",
    "Simple ",
    "Strange ",
    "Vivid ",
    "Godly ",
    "Demonic ",
    "Forceful ",
    "Hurtful ",
    "Keen ",
    "Strong ",
    "Superior ",
    "Unpleasant ",
    "Zealous ",
    "Silky ",
    "Bloody ",
    "Shaded ",
    "Sweet ",
    "Fruitful ",
    "Magnetic ",
    "Moil ",
    "Candied ",
    "Perfect ",
    "Wise "
]


def bin_auctions(KEY):
    for auction in get_auctions(KEY):
        # This removes pets as well
        if "bin" in auction and "[Lvl " not in auction["item_name"]:
            del (
                auction["uuid"], 
                auction["auctioneer"], 
                auction["profile_id"], 
                auction["coop"], 
                auction["start"], 
                auction["end"], 
                auction["item_lore"], 
                auction["extra"], 
                auction["bids"], 
                auction["item_bytes"], 
                auction["claimed_bidders"]
            )
        yield auction


def filter_item(auction):
        if "Wise Dragon" not in auction["item_name"] and "Perfect Chestplate" not in auction["item_name"] and "Perfect Helmet" not in auction["item_name"] and "Perfect Leggings" not in auction["item_name"] and "Perfect Boots" not in auction["item_name"] and "Absolutely Perfect" not in auction["item_name"]:
            for reforge in reforges:
                if reforge in auction["item_name"]:
                    auction["item_name"] = auction["item_name"].replace(reforge, "")
        if "Wise Dragon" in auction["item_name"] or "Very Wise Dragon" in auction["item_name"]:

            auction["item_name"] = auction["item_name"].replace("Very ",
            "")
            for reforge in reforges[:-1]:
                auction["item_name"] = auction["item_name"].replace(reforge, "")
        if "Perfect " in auction["item_name"]:
            auction["item_name"] = auction["item_name"].replace("Absolutely ",
            "")
            for reforge in reforges[:-2]:
                auction["item_name"] = auction["item_name"].replace(reforge, "")

        return auction["item_name"]


def sorted_by_name(key):
    sort = {}
    for auction in bin_auctions(key):
        name = filter_item(auction)
        if name is not None:
            if auction["item_name"] == name:
                sort[name] = sort.get(name, [])
                sort[name].append(auction)
    return sort


def get_flips(key):
    sort = sorted_by_name(key)
    for key in sort:
        cheapest = []
        for item in sort[key]:
            cheapest.append(int(item["starting_bid"]))
        cheapest = sorted(cheapest)[:2]
        if len(cheapest) == 2:
            difference = cheapest[1]*0.99 - cheapest[0]
            margin = round(difference/cheapest[0]*100, 1)
            yield {
                "Item Name": key, 
                "Buy Price": cheapest[0], 
                "Sell Price": cheapest[1]*0.99, 
                "Difference": difference, 
                "Profit Margin": margin
            }


def main(key):
    for flip in sorted(get_flips(key), key=lambda x: x['Difference']):
        Name = flip["Item Name"]
        Buy = flip["Buy Price"]
        Sell = round(flip["Sell Price"])
        Difference = round(flip["Difference"])
        Profit = flip["Profit Margin"]
        print(f"| Item Name: {Name} | Buy Price: {Buy} | Sell Price: {Sell} | Profit: {Difference} | Profit Margin: {Profit} |\n")
        

if __name__ == '__main__':
    main(get_key())