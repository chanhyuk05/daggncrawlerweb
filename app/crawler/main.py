import json

import click
import questionary

from app.crawler.crawl import get_items
from app.crawler.location import get_location


@click.command()
def crawl():
    region_keyword = questionary.text("크롤링할 지역명을 입력하세요:").ask()

    location_choices = get_location(region_keyword)

    if not location_choices:
        print("해당 지역에 대한 결과가 없습니다.")
        return

    if len(location_choices) == 1:
        loc = location_choices[0]
        location_id = f"{loc['name']}-{loc['id']}"
    else:
        selected_location = questionary.select(
            "지역을 선택하세요:",
            choices=[loc["label"] for loc in location_choices]
        ).ask()
        selected_loc = next(loc for loc in location_choices if loc["label"] == selected_location)
        location_id = f"{selected_loc['name']}-{selected_loc['id']}"
        
    print(f"선택된 지역: {location_id}")

    amount = int(questionary.text("크롤링할 아이템 수를 입력하세요 (기본값 10):", default="10").ask())
    keyword = questionary.text("검색어를 입력하세요:").ask()
    output = questionary.text("출력 파일명을 입력하세요 (기본값: output.csv):", default="output.csv").ask()

    results = get_items(location_id, amount, keyword, output)
    
    print('results', json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    crawl()