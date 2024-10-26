import os
from symtable import Class

import httpx

class GetDataService:

    @staticmethod
    async def getData():
        API_KEY = os.environ.get('OPEN_API_KEY')
        API_RETURN_TYPE = 'json'
        API_SIDO = '전국'
        API_VERSION = '1.5'

        res = httpx.get(f'https://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?serviceKey={API_KEY}&returnType={API_RETURN_TYPE}&numOfRows=1000&pageNo=1&sidoName={API_SIDO}&ver={API_VERSION}')
        return res.json()