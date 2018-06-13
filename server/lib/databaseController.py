import mysql.connector as mariadb
#from userController import user
import  json
import time
import datetime

PROD_ID = 0
PROD_USER_ID = 1
PROD_TITLE = 2
PROD_DESCRIPTION = 3
PROD_CONDITIE = 4
PROD_COUNTRY = 5
PROD_STATE = 6
PROD_CITY = 7
PROD_IS_AUCTION = 8
PROD_PRICE = 9
PROD_SHIPPING_TYPE = 10
PROD_SHIPPING_PRICE = 11
PROD_DATE_ADDED = 12
PROD_DATE_EXPIRES = 13
PROD_CATEGORY = 14
PROD_SUBCATEGORY =15
PROD_VIEWS = 16
PROD_STATUS =17

USER_ID =0
USER_USERNAME = 1
USER_PASSWORD =2
USER_FIRST_NAME = 3
USER_LAST_NAME =4
USER_EMAIL =5
USER_COUNTRY =6
USER_STATE =7
USER_CITY = 8
USER_ADRESS_1 =9
USER_ADRESS_2 =10
USER_ZIP_CODE =11
USER_CONTACT_INFO = 12
USER_CELL_NUMBER =13
USER_STATUS =14
USER_SALT =15

import databaseCredentials
mariadb_connection = mariadb.connect(user=databaseCredentials.user, password=databaseCredentials.password, host='localhost', database='tw')
mycursor = mariadb_connection.cursor()


class databaseController():

    def executeSQLCommand(self,command,commit):
        mycursor.execute(command)
        result = mycursor.fetchall()
        if commit == True:
            mariadb_connection.commit()
        return result

    """Extracting basic data from tables"""
    def getItemsFromTable(self, table, column, key, *args):
        command = None
        if len(args)==0:
            if(isinstance(key,basestring)):
                command = "SELECT * FROM {table} WHERE {column}='{key}'".format(key=key,table=table,column=column)
            else:
                command = "SELECT * FROM {table} WHERE {column}={key}".format(key=key, table=table, column=column)
        mycursor.execute(command)
        result = mycursor.fetchall()
        return result

    def getUserById(self,key):
        return self.getItemsFromTable('user','user_id',key)

    def getUserByEmail(self,key):
        return self.getItemsFromTable('user','email',key)

    def getUserbidByID(self,key):
        return self.getItemsFromTable('userbid','current_bid_id',key)

    def getTransactionById(self,key):
        return self.getItemsFromTable('transaction','transaction_id',key)

    def getResponseById(self,key):
        return self.getItemsFromTable('response','response_id',key)

    def getReportById(self,key):
        return self.getItemsFromTable('report','report_id',key)

    def getQuestionById(self,key):
        return self.getItemsFromTable('question','question_id',key)

    def getProductDataById(self,key):
        return self.getItemsFromTable('productdata','product_data_id',key)

    def getProducts(self):
        command= "select * from productdata"
        mycursor.execute(command)
        result = mycursor.fetchall()
        return result

    def getNoticeById(self,key):
        return self.getItemsFromTable('notice','notice_id',key)

    def getFeedbackById(self,key):
        return self.getItemsFromTable('feedback','feedback_id',key)

    def getSessionById(self,key):
        return self.getItemsFromTable('sessions','session_id',key)

    def getDate(self,table,column_key,column_date,key):
        command = "select '{column_date}' from '{table}' where {column_key}={key}".format(
            column_date=column_date,table=table,column_key=column_key,key=key
        )
        mycursor.execute(command)
        result = mycursor.fetchall()
        return result

    def getUserByUsername(self,key):
        command = "select * from user where username='{key}'".format(key=key)
        mycursor.execute(command)
        result = mycursor.fetchone()
        return result

    def getUserProducts(self,key):
        command = "select * from productdata where user_id={key}".format(key=key)
        mycursor.execute(command)
        result = mycursor.fetchall()
        return result

    def getImages(self,key):
        command = "select image from images where product_data_id={key}".format(key=key)
        mycursor.execute(command)
        result = mycursor.fetchall()
        list = []
        for i in result:
            list.append(i[0])
        return list

    #def advancedSearch(self):

    """Inserting data into tables"""
    def insertIntoUser(self, info):
        lista = [info["username"],info["password"],info["first_name"],info["last_name"],info["email"],info["country"],info["state"],info["city"],info["adress_1"],info["adress_2"],info["zip_code"],info["contact_info"],info["cell_number"],info["status"],info["salt"]]
        command = "INSERT INTO user(username,password,first_name,last_name,email,country,state,city,adress_1,adress_2,zip_code,contact_info,cell_number,status,salt) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(command,lista)
        mariadb_connection.commit()

    def insertIntoUserbid(self, info):
        lista = [info["user_id"],info["product_id"],info["status"],info["value"]]
        command = "INSERT INTO userbid(user_id,product_id,status,value) VALUES(%s,%s,%s,%s)"
        mycursor.execute(command,lista)
        mariadb_connection.commit()

    def insertIntoProductdata(self,info):
        lista = [info["user_id"],info["title"],info["description"],info["conditie"],info["country"],info["state"],info["city"],info["is_auction"],info["price"],info["shipping_type"],info["shipping_price"],info["date_added"],info["date_expires"],info["category"],info["subcategory"],info["views"],info["status"]]
        command = "INSERT INTO productdata(user_id,title,description,conditie,country,state,city,is_auction,price,shipping_type,shipping_price,date_added,date_expires,category,subcategory,views,status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(command,lista)
        mariadb_connection.commit()
        command="select max(product_data_id) from productdata"
        mycursor.execute(command)
        result=mycursor.fetchone()
        hashmap={
            "product_data_id" : result[0],
            "image" : info["image"]
        }
        self.insertIntoImages(hashmap)


    def insertIntoFeedback(self,info):
        lista = [info["transaction_id"],info["user_id"],info["title"],info["content"]]
        command = "INSERT INTO feedback(transaction_id,user_id,rating,title,content) VALUES(%s,%s,%s,%s)"
        mycursor.execute(command,lista)
        mariadb_connection.commit()

    def insertIntoImages(self,info):
        for i in info["image"]:
            lista = [info["product_data_id"], i]
            command = "INSERT INTO images(product_data_id,image) VALUES(%s,%s)"
            mycursor.execute(command, lista)
            mariadb_connection.commit()

    def insertIntoNotice(self,info):
        lista = [info["for_user_id"],info["from_user_id"],info["notice"],info["title"],info["content"]]
        command = "INSERT INTO notice(for_user_id,from_user_id,count,title,content) VALUES(%s,%s,%s,%s,%s)"
        mycursor.execute(command,lista)
        mariadb_connection.commit()

    def insertIntoQuestion(self,info):
        lista = [info["product_id"],info["user_id"],info["title"],info["content"]]
        command = "INSERT INTO question(product_id,user_id,title,content}) VALUES(%s,%s,%s,%s)"
        mycursor.execute(command,lista)
        mariadb_connection.commit()

    def insertIntoReport(self,info):
        lista = [info["type"],info["from_uid"],info["to_uid"],info["product_id"],info["reason"],info["details"],info["resolved"],info["date_resolved"],info["is_valid"]]
        command = "INSERT INTO report(type,from_uid,to_uid,product_id,reason,details,resolved,date_resolved,is_valid) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(command,lista)
        mariadb_connection.commit()

    def insertIntoResponse(self,info):
        lista = [info["product_id"],info["user_id"],info["title"],info["content"]]
        command = "INSERT INTO response(product_id,user_id,title,content) VALUES(%s,%s,%s,%s)"
        mycursor.execute(command,lista)
        mariadb_connection.commit()

    def insertIntoTrasnaction(self,info):
        lista = [info["seller_user_id"],info["buyer_user_id"],info["product_id"],info["has_ended"],datetime.datetime.now(),self.getDate('productdata','product_data_id','date_expires',info["product_id"])]
        command = "INSERT INTO transaction(seller_user_id,buyer_user_id,product_id,has_ended,date_initiated,date_ended) VALUES(%s,%s,%s,%s,%,s.%s)"
        mycursor.execute(command,lista)
        mariadb_connection.commit()
        hashmap={
            "user_id" : info["buyer_user_id"],
            "product_id" : info["product_id"],
            "status" : 'ongoing',
            "value" : info["value"]
        }
        self.insertIntoUserbid(hashmap)

    def insertIntoSessions(self,info):
        command = "INSERT INTO sessions VALUES({session_id}, {user_id}, {date_created}, {last_connected}, '{device}', '{ip}')".format(
            session_id=info["session_id"], user_id=info["user_id"], date_created=info["date_created"],
            last_connected=info["last_connected"], device=info["device"], ip=info["ip"]
        )
        mycursor.execute(command)
        mariadb_connection.commit()

    """Setari inactiv in baza de date"""

    def setInactiveInTransaction(self, key):
        command = "UPDATE transaction set has_ended ='ended' where product_id_id={key}".format(key=key)
        mycursor.execute(command)
        mariadb_connection.commit()

    def setInactiveInUserbid(self, key):
        command = "update userbid set status='lost' where product_id={key})".format(key=key)
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "select current_bid_id from userbid where value=max(value)"
        mycursor.execute(command)
        result = mycursor.fetchone()
        command = "update userbid set status='won' where current_bid_id={result}".format(result=result)
        mycursor.execute(command)
        mariadb_connection.commit()

    def setInactiveInUser(self, key):
        command = "update user set status='inactive' where user_id={key}".format(key=key)
        mycursor.execute(command)
        mariadb_connection.commit()

    def setInactiveInProduct(self, key):
        command = "update product set status='sold' where product_data_id={key})".format(key=key)
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "select product_id where product_id={key}".format(key=key)
        mycursor.execute(command)
        result = mycursor.fetchone()
        self.setInactiveInTransaction(result)
        self.setInactiveInUserbid(result)

    """Delete everything in database"""
    def resetAutoIncrement(self):
        command = "alter table user AUTO_INCREMENT = 1"
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "alter table userbid AUTO_INCREMENT = 1"
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "alter table transaction AUTO_INCREMENT = 1"
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "alter table sessions AUTO_INCREMENT = 1"
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "alter table response AUTO_INCREMENT = 1"
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "alter table report AUTO_INCREMENT = 1"
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "alter table question AUTO_INCREMENT = 1"
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "alter table productdata AUTO_INCREMENT = 1"
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "alter table notice AUTO_INCREMENT = 1"
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "alter table images AUTO_INCREMENT = 1"
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "alter table feedback AUTO_INCREMENT = 1"
        mycursor.execute(command)
        mariadb_connection.commit()

    def deleteDatabase(self):
        command = "delete from userbid"
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "delete from transaction"
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "delete from sessions"
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "delete from report"
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "delete from question"
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "delete from images"
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "delete from productdata"
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "delete from feedback"
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "delete from notice"
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "delete from response"
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "delete from user"
        mycursor.execute(command)
        mariadb_connection.commit()
        self.resetAutoIncrement()

    """Match chestii"""
    def matchText(self,info):
        command = "select product_data_id from productdata where match(title,description,category,subcategory) against('{info}') order by match(title,description,category,subcategory) against('{info}') desc".format(info=info)
        mycursor.execute(command)
        result = mycursor.fetchall()
        return result

    """Get products by filter"""
    def getProductsByFilter(self,info,order_by,how,query):
        where_clause = ""
        order = ""
        how_order = "asc"
        for key,value in info.items():
            if value != None and value != "":
                if key == 'min_price':
                     where_clause += "and price>={min_price} ".format(min_price=value)
                elif key == 'max_price':
                    where_clause += "and price<={max_price} ".format(min_price=value)
                elif isinstance(value,int):
                    where_clause =where_clause + "and {key}={value} ".format(key=key, value=value)
                elif isinstance(value,basestring):
                    where_clause =where_clause + "and '{key}'='{value}' ".format(key=key, value=value)
        if order_by != None and order_by!= "":
            order+="order by '{what}'".format(what=order_by)
        if how == "desc":
            how_order = "desc"
        command = "select product_data_id from productdata where (match(title,description,category,subcategory) against( '{query}' )) {clause} {order_by} {how},(match (title,description,category,subcategory) against ('{query}')) desc".format(
            clause=where_clause, query=query, order_by=order, how=how_order
        )
        mycursor.execute(command)
        result = mycursor.fetchall()
        return result

    """Set new session id"""
    def removeSessionId(self,session):
        command = "delete from sessions where session_id={session}".format(session=session)
        mycursor.execute(command)
        mariadb_connection.commit()


if __name__ == "__main__":
    metod = databaseController()

    #print json.dumps(metod.getUserById("user","country","'romania'"),indent=4)

    hashinfo={
        "username":'aa',
        "password":'aaaa',
        "first_name": 'bbb',
        "last_name": 'ccc',
        "email":'ddd',
        "country":'eee',
        "state":'ffff',
        "city":'gggg',
        "adress_1":'hhhh',
        "adress_2":'iiii',
        "zip_code":'jjj',
        "contact_info":'dadfds',
        "cell_number":'asdsfsd',
        "status":'asfdfds',
        "salt":bytearray("dawdas")
    }
    #metod.insertIntoUser(hashinfo)
    prodData = {'title': 'Air guitar Epiphone les paul vasilescu',
                'description': 'cea mia mijtoui s mora mama meu k ii sm3k mkatzash lorem gipsum jajaj jaj as lal qea j2qj h n asdasd, asdasldkj',
                'conditie': 3,
                'country': 'vaslui kong',
                'state': 'triburile romane unite',
                'city': 'vaslui',
                'is_auction': 1,
                'price': 399,
                'shipping_type': 'Malaysia Airways',
                'shipping_price': 429,
                'date_added': datetime.datetime.now(),
                'date_expires': datetime.datetime.now(),
                'category': 'lol nu stiu',
                'subcategory': 'yes',
                'views': 420,
                'image': [bytearray('asdasdasd'),bytearray('sdagfdgfds')],
                'user_id': 1,
                'status':'ongoing'
                }
    #print(hashinfo["condition"])
    #metod.insertIntoProductdata(prodData)
    print metod.getProductDataById(1)
    #print json.dumps(metod.matchText("Gabi"),indent=4)
    #print metod.getProductsByFilter(hashinfo,'condition','asc','aaa')
    #metod.deleteDatabase()

databaseController = databaseController()


