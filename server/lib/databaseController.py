import mysql.connector as mariadb
import  json
import time
import datetime
mariadb_connection = mariadb.connect(user='root', password='mancare', host='localhost', database='tw')
mycursor = mariadb_connection.cursor()


class databaseController():

    def executeSQLCommand(self,command):
        mycursor.execute(command)
        mariadb_connection.commit()

    """Extracting basic data from tables"""
    def getItemsFromTable(self, table, column, key, *args):
        command = None
        print args
        if len(args)==0:
            command = "SELECT * FROM {table} WHERE {column}={key}".format(key=key,table=table,column=column)
        print command
        mycursor.execute(command)
        items = mycursor.fetchall()
        result = list()
        for item in items:
            row = dict(zip(mycursor.column_names, item))
            result.append(row)
        return result

    def getUserById(self,key):
        return self.getItemsFromTable('user','user_id',key)

    def getUserbidByID(self,key):
        return self.getItemsFromTable('userbid','xurrent_bid_id',key)

    def getUserproductById(self,key):
        return self.getItemsFromTable('userproduct','user_prod_id',key)

    def getTransactionById(self,key):
        return self.getItemsFromTable('transaction','transaction_id',key)

    def getResponseById(self,key):
        return self.getItemsFromTable('response','response_id',key)

    def getReportById(self,key):
        return self.getItemsFromTable('report','report_id',key)

    def getQuestionById(self,key):
        return self.getItemsFromTable('question','question_id',key)

    def getProductDataById(self,key):
        return self.getItemsFromTable('product_data','product_data_id',key)

    def getProductById(self,key):
        return self.getItemsFromTable('product','product_id',key)

    def getNoticeById(self,key):
        return self.getItemsFromTable('notice','notice_id',key)

    def getFeedbackById(self,key):
        return self.getItemsFromTable('feedback','feedback_id',key)

    def getSessionById(self,key):
        return self.getItemsFromTable('sessions','session_id',key)


    #def advancedSearch(self):

    """Inserting data into tables"""
    def insertIntoUser(self, info):
        lista = [info["username"],info["password"],info["first_name"],info["last_name"],info["email"],info["country"],info["state"],info["city"],info["adress_1"],info["adress_2"],info["zip_code"],info["contact_info"],info["cell_number"],info["session_id"]]
        command = "INSERT INTO user(username,password,first_name,last_name,email,country,state,city,adress_1,adress_2,zip_code,contact_info,cell_number,session_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(command,lista)
        mariadb_connection.commit()

    def insertIntoUserbid(self, info):
        lista = [info["user_id"],info["product_id"]]
        command = "INSERT INTO userbid(user_id,product_id) VALUES(%s,%s)"
        mycursor.execute(command,lista)
        mariadb_connection.commit()

    def insertIntoProduct(self,info):
        lista = [info["user_id"],info["product_data_id"],info["title"]]
        command = "INSERT INTO product(user_id,product_data_id,title) VALUES(%s,%s,%s)"
        mycursor.execute(command,lista)
        mariadb_connection.commit()

    def insertIntoProductdata(self,info):
        lista = [info["title"],info["desc"],info["contition"],info["country"],info["city"],info["is_auction"],info["price"],info["shipping_type"],info["shipping_price"],info["image"],info["date_added"],info["date_expires"],info["category"],info["subcategory"]]
        command = "INSERT INTO productdata(title,desc,condition,country,city,is_auction,price,shipping_type,shipping_price,image,date_added,date_expires,category,subcategory) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(command,lista)
        mariadb_connection.commit()

    def insertIntoFeedback(self,info):
        lista = [info["transaction_id"],info["user_id"],info["title"],info["content"]]
        command = "INSERT INTO feedback(transaction_id,user_id,rating,title,content) VALUES(%s,%s,%s,%s)"
        mycursor.execute(command,lista)
        mariadb_connection.commit()

    def insertIntoImage(self,info):
        for i in info["image"]:
            lista = [info["user_id"],i]
            command = "INSERT INTO images(user_id,image) VALUES(%s,%s)"
            mycursor.execute(command,lista)
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
        lista = [info["seller_user_id"],info["buyer_user_id"],info["has_ended"],info["date_initiated"],info["date_ended"]]
        command = "INSERT INTO transaction(seller_user_id,buyer_user_id,has_ended,date_initiated,date_ended) VALUES()"
        mycursor.execute(command,lista)
        mariadb_connection.commit()

    def insertIntoSessions(self,info):
        command = "INSERT INTO sessions VALUES({session_id}, {user_id}, {date_created}, {last_connected}, '{device}', '{ip}')".format(
            session_id=info["session_id"], user_id=info["user_id"], date_created=info["date_created"],
            last_connected=info["last_connected"], device=info["device"], ip=info["ip"]
        )



metod = databaseController()

#print json.dumps(metod.getUserById("user","country","'romania'"),indent=4)

hashinfo={
    "username" : 'GabiHartobanu',
    "password" : 'mancare',
    "first_name" : 'Hirtobanu',
    "last_name" : 'Gabi',
    "email" : 'gabi@yahoo.com',
    "country" : 'romania',
    "state" : '',
    "city" : 'iasi',
    "adress_1" : 'ciurbesti_1',
    "adress_2" : 'ciurbesti2',
    "zip_code" : '11111',
    "contact_info" : 'contact1',
    "cell_number" : '0766******',
    "session_id" : 12
}

#metod.insertIntoUser(hashinfo)
print metod.getUserById(1)
#rec = [12.0,'acum']
#mycursor.execute("insert into testare(ceva,ceva2) values (%s,%s)", rec)
#mariadb_connection.commit()


#record = ['GabiHartobanu','mancare','Hirtobanu','Gabriel','gabi@yahoo.com','romania','','iasi','ciurebesti1','ciurbesti2','111','contacti1','0753******',7]
#mycursor.execute('insert into user(username,password,first_name,last_name,email,country,state,city,adress_1,adress_2,zip_code,contact_info,cell_number,session_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%d)',record )
#mariadb_connection.commit()
#print mycursor.fetchall()
#mycursor.execute('INSERT INTO userbid VALUES (1,1,1)')
#mariadb_connection.commit()
