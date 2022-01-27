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
    def get_link_scraping(cls,page):
        print(page)
        result = BaseResponse()
        result.status = 400
        try:
            #mengambil data dalam sebuah page
            data = link_news(int(page)).get_single_link()
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
    def get_data_scraping(cls,page):
        db = SessionLocal()
        result = BaseResponse()
        result.status = 400
        hasil = []
        #menambahkan no sesuai dengan input no terakhir
        no = conn.table('records').max('no')
        if no is None:
            no = 0
        try:
            for i in range(0,(int(page))*9):
                data = news_scraping(link_news(int(page)).get_single_link()[i]).get_news()
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

    @classmethod
    def insert_data_scraping_csv(cls,input_data):
        db = SessionLocal()
        result = BaseResponse()
        result.status = 400
        hasil = []
        try:
            file_location = input_data['file_location']
            with open(str(file_location), "r") as f:
                csv_reader = csv.DictReader(f)
                for row in csv_reader:
                    #case jika data url atau no match dengan data di database
                    if conn.table('records').where('no','=',row['no']).or_where('url','=',row['url']).first():
                        row['status'] = 404
                        row['message'] = "data is already in database"
                        hasil.append(row)    
                    else:
                    #case jika data url atau no belum ada di database
                        row['status'] = 200
                        row['message'] = "database input success"
                        db_record = ScrapingModels.Record(
                            no=row["no"],
                            title=row["title"].strip(),
                            author=row["author"],
                            date=row["date"],
                            content=row["content"],
                            link_picture=row['link_picture'],
                            url =row['url']
                        )
                        db.add(db_record)
                        db.commit()
                        hasil.append(row)
                result.data = {"hasil":hasil} 
                result.status = 200
                result.message = "success"
                Log.info(result.message) 
        except Exception as e:
            Log.error(e)
            result.status = 400
            result.message = str(e)
        db.close()
        return result





        
