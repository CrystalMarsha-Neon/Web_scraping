import json
from apps.controllers.ScrapingController import ControllerScraping as scraping
from fastapi import APIRouter, Body, Response
from typing import Optional

from fastapi import APIRouter, Query, Response
router = APIRouter()

example_input_location = json.dumps({
    "file_location": "C:/Users/User/Downloads/de/News_Scraping/test_1.csv"
}, indent=2)

example_input_data = json.dumps({
    "no": "5",
    "author": "Achmad Dwi Afriyadi - detikFinance"
}, indent=2)
@router.post("/get_link_scraping")
async def get_link_scraping(response: Response, 
        page: Optional[int]=Query(None)):
    result = scraping.get_link_scraping(page=page)
    response.status_code = result.status
    return result

@router.post("/get_data_scraping")
async def get_data_scraping(response: Response, 
        page: Optional[int]=Query(None)):
    result = scraping.get_data_scraping(page=page)
    response.status_code = result.status
    return result

@router.post("/get_data_from_database")
async def get_data_from_database(response: Response,
        input_data = Body(...,example=example_input_data)):
    result = scraping.get_data_from_database(input_data=json.loads(input_data))
    response.status_code = result.status
    return result

@router.post("/insert_data_scraping_csv")
async def insert_data_scraping_csv(response: Response,
        input_data = Body(...,example=example_input_location)):
    result = scraping.insert_data_scraping_csv(input_data = json.loads(input_data))
    response.status_code = result.status
    return result
