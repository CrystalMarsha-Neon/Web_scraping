import json
from apps.controllers.ScrapingController import ControllerScraping as scraping
from fastapi import APIRouter, Body, Response
from typing import Optional

from fastapi import APIRouter, Query, Response
router = APIRouter()

example_input_data = json.dumps({
    "no": "5",
    "author": "Achmad Dwi Afriyadi - detikFinance"
}, indent=2)
@router.post("/get_link_scraping")
async def get_link_scraping(response: Response, 
        start_page: Optional[int]=Query(None),
        end_page: Optional[int]=Query(None)):
    result = scraping.get_link_scraping(start_page=start_page,end_page=end_page)
    response.status_code = result.status
    return result

@router.post("/get_data_scraping")
async def get_data_scraping(response: Response, 
        start_page: Optional[int]=Query(None),
        end_page: Optional[int]=Query(None)):
    result = scraping.get_data_scraping(start_page=start_page,end_page=end_page)
    response.status_code = result.status
    return result

@router.post("/get_data_from_database")
async def get_data_from_database(response: Response,
        input_data = Body(...,example=example_input_data)):
    result = scraping.get_data_from_database(input_data=input_data)
    response.status_code = result.status
    return result
