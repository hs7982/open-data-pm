from fastapi import APIRouter

from service.getData import GetDataService

getData_Router = APIRouter()

@getData_Router.get('/getData')
async def get_data():
    return await GetDataService.getData()