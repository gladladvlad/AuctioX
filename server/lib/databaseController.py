import mysql.connector as mariadb
#from userController import user
import  json
import time
import datetime
from util import *

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
PROD_CURRENCY = 10
PROD_SHIPPING_TYPE = 11
PROD_SHIPPING_PRICE = 12
PROD_DATE_ADDED = 13
PROD_DATE_EXPIRES = 14
PROD_CATEGORY = 15
PROD_SUBCATEGORY = 16
PROD_VIEWS = 17
PROD_STATUS = 18

USER_ID = 0
USER_USERNAME = 1
USER_PASSWORD = 2
USER_FIRST_NAME = 3
USER_LAST_NAME = 4
USER_EMAIL = 5
USER_COUNTRY = 6
USER_STATE = 7
USER_CITY = 8
USER_ADRESS_1 = 9
USER_ADRESS_2 = 10
USER_ZIP_CODE = 11
USER_CONTACT_INFO = 12
USER_CELL_NUMBER = 13
USER_STATUS = 14
USER_SALT = 15
USER_ADMIN = 16

BID_ID = 0
BID_USER_ID = 1
BID_PROD_ID = 2
BID_STATUS =3
BID_VALUE = 4

TRANSACTION_ID = 0
TRANSACTION_SELLER_ID = 1
TRANSACTION_BUYER_ID = 2
TRANSACTION_PRODUCT_ID = 3
TRANSACTION_STATUS = 4
TRANSACTION_DATE_CREATED = 5
TRANSACTION_DATE_EXPIRES = 6
TRANSACTION_SELLER_CONFIRM = 7
TRANSACTION_BUYER_CONFIRM = 8

QUESTION_ID = 0
QUESTION_PRODUCT_ID = 1
QUESTION_USER_ID = 2
QUESTION_ANSWER_KEY = 3
QUESTION_CONTENT = 4

RESPONSE_ID = 0
RESPONSE_PRODUCT_ID = 1
RESPONSE_USER_ID = 2
RESPONSE_ANSWER_KEY = 3
RESPONSE_CONTENT = 4

REPORT_ID = 0
REPORT_TYPE = 1
REPORT_FROM = 2
REPORT_TO = 3
REPORT_PRODUCT_ID = 4
REPORT_REASON = 5
REPORT_DETAILS = 6
REPORT_RESOLVED = 7
REPORT_DATE_RESOLVED = 8
REPORT_IS_VALID = 9

import databaseCredentials
mariadb_connection = mariadb.connect(user=databaseCredentials.user, password=databaseCredentials.password, host='localhost', database='tw')
mycursor = mariadb_connection.cursor()


class databaseController():

    def executeSQLCommand(self, command, commit=False):
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
        logger.debug("")
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

    def getTransactionBySellerId(self, userID):
        command= "select * from transaction join user on seller_user_id = {0} and user_id = {0} and not has_ended = \"ended\"".format(userID)
        mycursor.execute(command)
        result = mycursor.fetchall()
        return result

    def getTransactionByBuyerId(self, userID):
        command= "select * from transaction join user on buyer_user_id = {0} and user_id = {0} and not has_ended = \"ended\"".format(userID)
        mycursor.execute(command)
        result = mycursor.fetchall()
        return result

    def getResponseById(self,key):
        return self.getItemsFromTable('response','response_id',key)

    def getReportById(self,key):
        return self.getItemsFromTable('report','report_id',key)

    def getReportByToUserId(self, userID):
        command= "select * from report where to_uid = {0} and is_valid = 1".format(userID)
        mycursor.execute(command)
        result = mycursor.fetchall()
        return result

    def getReportByFromUserId(self, userID):
        command= "select * from report where from_uid = {0} and is_valid = 1".format(userID)
        mycursor.execute(command)
        result = mycursor.fetchall()
        return result

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
        command = "select {column_date} from {table} where {column_key}={key}".format(
            column_date=column_date,table=table,column_key=column_key,key=key
        )
        mycursor.execute(command)
        result = mycursor.fetchone()
        return result[0]

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

    def getBidById(self, bidId):
        command = "select * from userbid where current_bid_id = {0}".format(bidId)
        mycursor.execute(command)
        result = mycursor.fetchall()
        return result[0]

    def getUserBidProduct(self,user_id):
        command = "select * from productdata join userbid on productdata.product_data_id= userbid.product_id where userbid.user_id={user_id}".format(user_id=user_id)
        print(command)
        mycursor.execute(command)
        result=mycursor.fetchall()
        return result

    def getBiggestBidForProduct(self,prod_id):
        command = "select max(value) from userbid where product_id={id}".format(
            id=prod_id
        )
        mycursor.execute(command)
        result = mycursor.fetchone()
        return result

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
        lista = [info["user_id"],info["title"],info["description"],info["conditie"],info["country"],info["state"],info["city"],info["is_auction"],info["price"],info["currency"],info["shipping_type"],info["shipping_price"],info["date_added"],info["date_expires"],info["category"],info["subcategory"],info["views"],info["status"]]
        command = "INSERT INTO productdata(user_id,title,description,conditie,country,state,city,is_auction,price,currency,shipping_type,shipping_price,date_added,date_expires,category,subcategory,views,status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
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
        return result[0]


    def insertIntoFeedback(self,info):
        lista = [info["transaction_id"],info["user_id"],info["rating"],info["title"],info["content"]]
        command = "INSERT INTO feedback(transaction_id,user_id,rating,title,content) VALUES(%s,%s,%s,%s,%s)"
        mycursor.execute(command,lista)
        mariadb_connection.commit()

    def insertIntoImages(self,info):
        for i in info["image"]:
            lista = [info["product_data_id"], i]
            command = "INSERT INTO images(product_data_id,image) VALUES(%s,%s)"
            mycursor.execute(command, lista)
            mariadb_connection.commit()

    def insertIntoNotice(self,info):
        lista = [info["for_user_id"],info["from_user_id"],info["count"],info["title"],info["content"]]
        command = "INSERT INTO notice(for_user_id,from_user_id,count,title,content) VALUES(%s,%s,%s,%s,%s)"
        mycursor.execute(command,lista)
        mariadb_connection.commit()

    def insertIntoQuestion(self,info):
        lista = [info["product_id"],info["user_id"],info["title"],info["content"]]
        command = "INSERT INTO question (product_id,user_id,title,content) VALUES(%s,%s,%s,%s)"
        print(command)
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

    def insertIntoTransaction(self,info):
        current_date = datetime.datetime.now()
        date_expires = current_date + datetime.timedelta(weeks=2)
        lista = [info["seller_user_id"],info["buyer_user_id"],info["product_data_id"],info["has_ended"],current_date,date_expires]
        command = "INSERT INTO transaction(seller_user_id,buyer_user_id,product_id,has_ended,date_initiated,date_ended) VALUES(%s,%s,%s,%s,%s,%s)"
        mycursor.execute(command,lista)
        mariadb_connection.commit()

    def insertIntoSessions(self,info):
        lista=[info["session_id"],info["user_id"],info["date_created"],info["last_connected"],info["device"],info["ip"]]
        command = "INSERT INTO sessions (session_id, user_id, date_created, last_connected, device, ip) values (%s,%s,%s,%s,%s,%s)"
        print command
        mycursor.execute(command,lista)
        mariadb_connection.commit()

    """Setari inactiv in baza de date"""

    def setInactiveInTransaction(self, key):
        command = "UPDATE transaction set has_ended ='ended' where transaction_id={key}".format(key=key)
        mycursor.execute(command)
        mariadb_connection.commit()

    def setInactiveInUserbid(self, key):
        command = "update userbid set status='lost' where product_id={key}".format(key=key)
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "select current_bid_id from userbid where product_id={key} order by value desc".format(key=key)
        mycursor.execute(command)
        result = mycursor.fetchall()
        command = "update userbid set status='won' where current_bid_id={result}".format(result=result[0][0])
        mycursor.execute(command)
        mariadb_connection.commit()

    def setInactiveInUser(self, key):
        command = "update user set status='inactive' where user_id={key}".format(key=key)
        mycursor.execute(command)
        mariadb_connection.commit()

    def setInactiveInProduct(self, key):
        command = "update productdata set status='ended' where product_data_id={key}".format(key=key)
        mycursor.execute(command)
        mariadb_connection.commit()

    def setActiveInProduct(self, key):
        command = "update productdata set status='ongoing' where product_data_id={key}".format(key=key)
        mycursor.execute(command)
        mariadb_connection.commit()

    """Setari in baza de date"""

    def setSellerConfirm(self,user,produs):
        command = "update transaction set seller_confirm = 1 where seller_user_id={user} and product_id={produs}".format(
            user=user, produs=produs
        )
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "select buyer_confirm from transaction where seller_user_id={user} and product_id={produs}".format(
            user=user, produs=produs
        )
        mycursor.execute(command)
        result = mycursor.fetchone()
        if result[0] == 1:
            self.setInactiveInTransaction(produs)

    def setBuyerConfirm(self,user,product):
        command = "update transaction set buyer_confirm = 1 where buyer_user_id={user} and product_id={produs}".format(
            user=user, produs=product
        )
        #print(command)
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "select seller_confirm from transaction where buyer_user_id={user} and product_id={produs}".format(
            user=user, produs=product
        )
        mycursor.execute(command)
        result = mycursor.fetchone()
        if result[0] == 1:
            self.setInactiveInTransaction(product)

    def getIsAdminById(self, userId):
        command = "select is_admin from user where user_id={0}".format(userId)
        mycursor.execute(command)
        result= mycursor.fetchone()
        return result


    def setAdminPrivileges(self,id1,id2,what):
        command = "select user_id from user where user_id={id1} and is_admin=1".format(id1=id1)
        mycursor.execute(command)
        result= mycursor.fetchone()
        if result is None:
            print "Nu esti admin"
        else:
            command = "update user set is_admin = {privilege} where user_id={id2}".format(
                id2=id2, privilege=what
            )
            mycursor.execute(command)
            mariadb_connection.commit()

    """Diverse"""

    def incrementView(self,product):
        command = "update productdata set views = views +1 where product_data_id = {product}".format(product=product)
        mycursor.execute(command)
        mariadb_connection.commit()

    def setNewPrice(self,id_prod,new_price):
        command = "update productdata set price={new_price} where product_data_id={id}".format(
            new_price=new_price, id=id_prod
        )
        mycursor.execute(command)
        mariadb_connection.commit()

    def stergeBid(self,bid_id):
        command = "delete from userbid where current_bid_id={id}".format(
            id=bid_id
        )
        mycursor.execute(command)
        mariadb_connection.commit()

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
        command = "delete from feedback"
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
        command = "delete from response"
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "delete from productdata"
        mycursor.execute(command)
        mariadb_connection.commit()
        command = "delete from notice"
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
        if (info is None) and (order_by is None) and (how is None) and (query == ''):
            command = "select * from productdata where status = 'ongoing' order by views desc"
            mycursor.execute(command)
            result = mycursor.fetchall()
            return result
        elif (info is None) and (order_by is None) and (how is None) and (query != ''):
            command = "select * from productdata where (match(title,description,category,subcategory) against( '{query}' )) and status = 'ongoing' order by views desc".format(query=query)
            print command
            mycursor.execute(command)
            result =mycursor.fetchall()
            return result
        elif (info is None) and (order_by is not None) and (how is None) and (query != ''):
            command = "select * from productdata where (match(title,description,category,subcategory) against( '{query}' )) and status = 'ongoing' order by {orderby} asc, views desc".format(
                query=query, orderby=order_by
            )
            mycursor.execute(command)
            result = mycursor.fetchall()
            return result
        elif (info is None) and (order_by is not None) and (how is None) and (query == ''):
            command = "select * from productdata order by {orderby}".format(orderby=order_by)
            mycursor.execute(command)
            result = mycursor.fetchall()
            return result
        elif (info is None) and (order_by is not None) and (how is not None) and (query == ''):
            command = 'select * from productdata order by {orderby} {how}, views desc'.format(
                orderby=order_by, how=how
            )
            mycursor.execute(command)
            result = mycursor.fetchall()
            return result
        elif (info is None) and (order_by is not None) and (how is not None) and (query != ''):
            command = "select * from productdata where (match(title,description,category,subcategory) against( '{query}' )) and status = 'ongoing' order by {orderby} {how}, views desc".format(
                query=query, orderby=order_by, how=how
            )
            mycursor.execute(command)
            result = mycursor.fetchall()
            return result
        elif (info is not None) and (order_by is None) and (how is None) and (query == ''):
            for key, value in info.items():
                if value is not None and value != "":
                    if key == 'conditie' and len(value) != 0:
                        where_clause += "and ("
                        for i in value:
                            where_clause += "conditie={value} or ".format(value=i)
                        where_clause += "0=1) "
                    elif key == 'min_price':
                        where_clause += "and price>={min_price} ".format(min_price=value)
                    elif key == 'max_price':
                        where_clause += "and price<={max_price} ".format(max_price=value)
                    elif isinstance(value, int):
                        where_clause = where_clause + "and {key}={value} ".format(key=key, value=value)
                    elif isinstance(value, basestring):
                        where_clause = where_clause + "and {key}='{value}' ".format(key=key, value=value)
            command = "select * from productdata where 1=1 {where_clause} and status = 'ongoing' order by views desc".format(
                query=query, where_clause=where_clause
            )
            print(command)
            mycursor.execute(command)
            result = mycursor.fetchall()
            return result
        elif (info is not None) and (order_by is None) and (how is None) and (query != ''):
            for key, value in info.items():
                if value is not None and value != "":
                    if key == 'conditie' and len(value) != 0:
                        where_clause += "and ("
                        for i in value:
                            where_clause += "conditie={value} or ".format(value=i)
                        where_clause += "0=1) "
                    elif key == 'min_price':
                        where_clause += "and price>={min_price} ".format(min_price=value)
                    elif key == 'max_price':
                        where_clause += "and price<={max_price} ".format(max_price=value)
                    elif isinstance(value, int):
                        where_clause = where_clause + "and {key}={value} ".format(key=key, value=value)
                    elif isinstance(value, basestring):
                        where_clause = where_clause + "and {key}='{value}' ".format(key=key, value=value)
            command = "select * from productdata where (match(title,description,category,subcategory) against( '{query}' )) {where_clause} and status = 'ongoing' order by views desc".format(
                query=query, where_clause=where_clause
            )
            mycursor.execute(command)
            result = mycursor.fetchall()
            return result
        elif (info is not None) and (order_by is not None) and (how is None) and (query == ''):
            for key, value in info.items():
                if value is not None and value != "":
                    if key == 'conditie' and len(value) != 0:
                        where_clause += "and ("
                        for i in value:
                            where_clause += "conditie={value} or ".format(value=i)
                        where_clause += "0=1) "
                    elif key == 'min_price':
                        where_clause += "and price>={min_price} ".format(min_price=value)
                    elif key == 'max_price':
                        where_clause += "and price<={max_price} ".format(max_price=value)
                    elif isinstance(value, int):
                        where_clause = where_clause + "and {key}={value} ".format(key=key, value=value)
                    elif isinstance(value, basestring):
                        where_clause = where_clause + "and {key}='{value}' ".format(key=key, value=value)
            command = "select * from productdata where 1=1 {clause} order by {order} asc, views desc".format(
                clause=where_clause, order=order_by
            )
            mycursor.execute(command)
            result = mycursor.fetchall()
            return result
        elif (info is not None) and (order_by is not None) and (how is None) and (query != ''):
            for key, value in info.items():
                if key == 'conditie' and len(value) != 0:
                    where_clause += "and ("
                    for i in value:
                        where_clause += "conditie={value} or ".format(value=i)
                    where_clause += "0=1) "
                elif value is not None and value != "":
                    if key == 'min_price':
                        where_clause += "and price>={min_price} ".format(min_price=value)
                    elif key == 'max_price':
                        where_clause += "and price<={max_price} ".format(max_price=value)
                    elif isinstance(value, int):
                        where_clause = where_clause + "and {key}={value} ".format(key=key, value=value)
                    elif isinstance(value, basestring):
                        where_clause = where_clause + "and {key}='{value}' ".format(key=key, value=value)
            command = "select * from productdata where (match(title,description,category,subcategory) against( '{query}' )) {clause} and status = 'ongoing' order by {order} asc, views desc".format(
                query=query, clause=where_clause, order=order_by
            )
            mycursor.execute(command)
            result = mycursor.fetchall()
            return result
        elif (info is not None) and (order_by is not None) and (how is not None) and (query == ''):
            for key, value in info.items():
                if value is not None and value != "":
                    if key == 'conditie' and len(value) != 0:
                        where_clause += "and ("
                        for i in value:
                            where_clause += "conditie={value} or ".format(value=i)
                        where_clause += "0=1) "
                    elif key == 'min_price':
                        where_clause += "and price>={min_price} ".format(min_price=value)
                    elif key == 'max_price':
                        where_clause += "and price<={max_price} ".format(max_price=value)
                    elif isinstance(value, int):
                        where_clause = where_clause + "and {key}={value} ".format(key=key, value=value)
                    elif isinstance(value, basestring):
                        where_clause = where_clause + "and {key}='{value}' ".format(key=key, value=value)
            command = "select * from productdata where 1=1 {clause} and status = 'ongoing' order by {order} {how}, views desc".format(
                clause=where_clause, order=order_by, how=how
            )
            mycursor.execute(command)
            result = mycursor.fetchall()
            return result
        elif (info is not None) and (order_by is not None) and (how is not None) and (query != ''):
            for key, value in info.items():
                if key=='conditie' and len(value)!=0:
                    where_clause+="and ("
                    for i in value:
                        where_clause+="conditie={value} or ".format(value=i)
                    where_clause+= "0=1) "
                elif value is not None and value != "":
                    if key == 'min_price':
                        where_clause += "and price>={min_price} ".format(min_price=value)
                    elif key == 'max_price':
                        where_clause += "and price<={max_price} ".format(max_price=value)
                    elif isinstance(value, int):
                        where_clause = where_clause + "and {key}={value} ".format(key=key, value=value)
                    elif isinstance(value, basestring):
                        where_clause = where_clause + "and {key}='{value}' ".format(key=key, value=value)
            command= "select * from productdata where (match(title,description,category,subcategory) against( '{query}' )) {clause} and status = 'ongoing' order by {order} {how}, views desc".format(
                query=query, clause=where_clause, order=order_by, how=how
            )
            print(command)
            mycursor.execute(command)
            result = mycursor.fetchall()
            return result


    """Set new session id"""
    def removeSessionId(self,session):
        command = "delete from sessions where session_id='{session}'".format(session=session)
        print(command)
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
                'conditie': 1,
                'country': 'spain',
                'state': '',
                'city': 'madrid',
                'is_auction': 1,
                'price': 367,
                'currency':'eur',
                'shipping_type': '',
                'shipping_price': 429,
                'date_added': datetime.datetime.now(),
                'date_expires': datetime.datetime.now(),
                'category': 'lol nu stiu',
                'subcategory': 'yes',
                'views': 445,
                'image': [bytearray('asdasdasd'),bytearray('sdagfdgfds')],
                'user_id': 3,
                'status':'ongoing'
                }
    #metod.insertIntoProductdata(prodData)
    #print metod.getUserByUsername('aa or 1=1')
    transactiondict={
        "seller_user_id":2,
        "buyer_user_id":3,
        "product_data_id":2,
        "has_ended":'ongoing',
        "value": 1000
    }
    session={
        "session_id": '42354fdsg5',
        "user_id":1,
        "date_created":datetime.datetime.now(),
        "last_connected":datetime.datetime.now(),
        "device":'aici',
        'ip':'1111'
    }
    reportmap={
        "type":'naspa',
        "from_uid":2,
        "to_uid":1,
        "product_id":1,
        "reason":15,
        "details":'nustiu deastea',
        "resolved":0,
        "date_resolved":datetime.datetime.now(),
        "is_valid":0
    }
    #metod.insertIntoReport(reportmap)
    response={
        "product_id":1,
        "user_id":2,
        "title":'intrebare',
        "content":'zi si mie'
    }
    #metod.insertIntoResponse(response)
    #metod.insertIntoQuestion(response)
    notice={
        "for_user_id":1,
        "from_user_id":2,
        "count":3,
        "title":'nu mai tin minte pt ce era asta',
        "content":"whaaaaaaaaaaaaaat?"
    }
    #metod.insertIntoNotice(notice)
    feedback={
        "transaction_id":1,
        "user_id":1,
        "rating":10,
        "title":'Nice',
        "content":'Super Nice'
    }
    #metod.insertIntoFeedback(feedback)
    #metod.insertIntoSessions(session)
    #print metod.getProductsByFilter({"conditie":[5,0]}, None, None, "")
    #print metod.getUserById(1)
    #metod.insertIntoTransaction(transactiondict)
    #metod.removeSessionId('+0rmdycrS81ncphLJWJK5A==')
    #metod.deleteDatabase()
    #metod.setInactiveInTransaction(1)
    #metod.setInactiveInProduct(1)
    #metod.setSellerConfirm(2,1)
    #metod.setBuyerConfirm(2,1)
    #print metod.getUserBidProduct(2)
    prod ={'category': u'Consumables', 'city': '', 'user_id': 1, 'description': u'wdasfaeger erh er her h',
     'date_expires': datetime.datetime(2018, 8, 14, 0, 0), 'title': u'wasd', 'country': '', 'price': u'13', 'views': 0,
     'is_auction': 1, 'currency': u'EUR', 'conditie': 1, 'state': '', 'status': 'ongoing',
     'shipping_type': '', 'date_added': datetime.datetime(2018, 6, 14, 11, 59, 54, 235000),
     'image': [u'data:image/png;base64,ZGF0YTppbWFnZS9wbmc7YmFzZ...GlWQk9SdzBLR2dvQUFBQU5TVWhFVWdBQU'],
     'shipping_price': 0, 'subcategory': ''}
    #metod.incrementView(2)
    #metod.setAdminPrivileges(3,4,0)
    #metod.insertIntoProductdata(prod)
    #metod.setInactiveInUser(1)
    #metod.setNewPrice(2,100)
    mapa={
        "user_id": 2,
        "product_id":2,
        "status":"ongoing",
        "value":100
    }
    #metod.insertIntoUserbid(mapa)
    #metod.stergeBid(1)
    #print metod.getBiggestBidForProduct(2)
    #metod.setBuyerConfirm(3,2)
    metod.setSellerConfirm(2,2)

databaseController = databaseController()


