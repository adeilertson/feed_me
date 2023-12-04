
# Known sources
def get_known_sources():
    known_sources = {
        'www.foodnetwork.com': 'food_network',
        'www.bonappetit.com': 'bon_appetit',
        'www.saltandlavender.com': 'salt_and_lavender',
        'www.delish.com': 'delish',
        'www.macheesemo.com': 'macheesemo'
    }
    return known_sources

def get_blank_recipie():
    # Blank recipe
    blank_recipe = {
        'error': '',
        'name': '',
        'chef': '',
        'yeild': 0,
        'url': '',
        'ingredients': [],
        'instructions': []
    }
    return blank_recipe
