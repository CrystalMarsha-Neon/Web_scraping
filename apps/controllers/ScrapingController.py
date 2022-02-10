from genericpath import exists
from apps.helper import Log
from apps.schemas import BaseResponse
from apps.models import ScrapingModels
from main import PARAMS
from apps.utils.news_scraping import news_scraping,link_news
from apps.models.database import SessionLocal,engine
from apps.models.OrmDatabase import conn
import csv

SALT = PARAMS.SALT.salt

class ControllerScraping(object):
    @classmethod
    def get_link_scraping(cls,start_page,end_page):
        result = BaseResponse()
        result.status = 400
        try:
            #mengambil data dalam sebuah page
            data = link_news(int(start_page),int(end_page)).get_single_link()
            result.status = 200
            result.message = "Success"
            result.data = {"link": data}
            Log.info(result.message)
        except Exception as e:
            Log.error(e)
            result.status = 400
            result.message = str(e)
        return result

    @classmethod
    def get_data_scraping(cls,start_page,end_page):
        db = SessionLocal()
        result = BaseResponse()
        result.status = 400
        hasil = []
        #menambahkan no sesuai dengan input no terakhir
        no = conn.table('records').max('no')
        if no is None:
            no = 0
        try:
            for i in range(0,(int(end_page)-int(start_page)+1)*9-1):
                data = news_scraping(link_news(int(start_page),int(end_page)).get_single_link()[i]).get_news()
                data['no'] =  no+i+1
                #case jika data url match dengan data di database
                if conn.table('records').where('url','=',data['url']).first(): 
                    data['status'] = 404
                    data['message'] = "data is already in database"
                    hasil.append(data)
                else:                    
                #case jika data url belum ada di database
                    data['status'] = 200
                    data['message'] = "database input success"
                    db_record = ScrapingModels.Record(no=data['no'],
                                title=data["title"],
                                author=data["author"],
                                date=data["date"],
                                content=data["content"],
                                link_picture=data['link_picture'],
                                url=data['url'])
                    db.add(db_record)
                    db.commit()  
                    hasil.append(data)
                result.data = {"latest_news":hasil} 
                result.status = 200
                result.message = "success"
                Log.info(result.message)    
        except Exception as e:
            Log.error(e)
            result.status = 400
            result.message = str(e)
        db.close()
        return result
    
    @classmethod
    def get_data_from_database(cls,input_data):
        result = BaseResponse()
        result.status = 400
        hasil = []
        try:
            #case kedua data tidak kosong
            if (input_data['no'] is not None and input_data['author'] is not None) and (input_data['no'] != "" and input_data['author'] != ""):
                data = conn.table('records').where('no','=',input_data['no']).where('author','=',input_data['author']).get()
                if len(data) != 0:
                    hasil.append(data)
                    result.status = 200
                    result.message = "Success"
                    result.data = {"get_data": hasil}
                    Log.info(result.message)
                #case data tidak kosong tidak match dengan data di database
                else:
                    e = "data not found"
                    Log.error(e)
                    result.status = 404
                    result.message = str(e)
            #case kedua data kosong
            elif (input_data['author'] is None and input_data['no'] is None) or (input_data['author'] == "" and input_data['no'] == ""):
                e = "there is no input data"
                Log.error(e)
                result.status = 404
                result.message = str(e)
            #case data no kosong
            elif input_data['no'] is None or input_data['no'] == "":
                data = conn.table('records').where('author','=',input_data['author']).get()
                hasil.append(data)
                result.status = 200
                result.message = "Success"
                result.data = {"get_data": hasil}
                Log.info(result.message)
            #case data author kosong
            elif input_data['author'] is None or input_data['author'] == "":
                data = conn.table('records').where('no','=',input_data['no']).get()
                hasil.append(data)
                result.status = 200
                result.message = "Success"
                result.data = {"get_data": hasil}
                Log.info(result.message)
            else:
                e = "data doesn't exists"
                Log.error(e)
                result.status = 404
                result.message = str(e)
        except Exception as e:
            Log.error(e)
            result.status = 400
            result.message = str(e)
        return result