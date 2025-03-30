import json
import os
import platform
import time
import click
import questionary

from fastapi import *
from crawl import get_items
from location import get_location
from save import save_as_excel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/crawl")
async def crawl(region_keyword: str, is_multiple_region: bool = False, amount: int = 10, keyword: str = None, start_price: int = None, end_price: int = None):
    if not is_multiple_region:
        location_choices = get_location(region_keyword)
        
        if not location_choices:
            print("해당 지역에 대한 결과가 없습니다.")
            return

        if len(location_choices) == 1:
            loc = location_choices[0]
            location_id = f"{loc['name']}-{loc['id']}"
            
    else:
        location_id = []
        
        location_choices = get_location(region_keyword)

        selected_locations = location_choices
        
        for selected_location in selected_locations:
            location_id.append(f"{selected_location['name']}-{selected_location['id']}")

    results = get_items(location_id, amount, keyword, start_price, end_price)
    return results

@app.get("/")
def read_root():
    return {"Hello": "World"}

# @click.command()

    # print(json.dumps(results, ensure_ascii=False , indent=2))
    #==================================엑셀 파일 저장==================================================
    # save_as_excel(results)
    
    # print(f"output.xlsx 파일로 저장되었습니다.")
    
    # output_file = "output.xlsx"
    # if platform.system() == "Darwin":  # macOS
    #     os.system(f"open {output_file}")
    # elif platform.system() == "Windows":
    #     os.startfile(output_file)
    # else:  # Linux
    #     os.system(f"xdg-open {output_file}")
if __name__ == '__main__':
    crawl()
