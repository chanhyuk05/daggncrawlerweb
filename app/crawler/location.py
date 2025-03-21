import requests


def get_location(keyword: str):
    base_url = f'https://www.daangn.com/v1/api/search/kr/location?keyword={keyword}'
    response = requests.get(base_url)
    
    data = response.json()

    locations = [
        {
            "label": f"{loc['name1']} {loc['name2']} {loc['name3']}",
            "id": loc["id"],
            "name": loc["name"]
        }
        for loc in data.get('locations', [])
    ]

    return locations