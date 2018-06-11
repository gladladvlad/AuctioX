import mysql.connector as mariadb
import  json
mariadb_connection = mariadb.connect(user='root', password='mancare', host='localhost', database='tw')
mycursor = mariadb_connection.cursor()


class databaseController():

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

    def getUserById(self,table,column,key):
        return self.getItemsFromTable(table,column,key)

    def getUserbidByID(self,table,column,key):
        return self.getItemsFromTable(table,column,key)

    def getUserproductById(self,table,column,key):
        return self.getItemsFromTable(table,column,key)

    def getTransactionById(self,table,column,key):
        return self.getItemsFromTable(table,column,key)

    def getResponseById(self,table,column,key):
        return self.getItemsFromTable(table,column,key)

    def getReportById(self,table,column,key):
        return self.getItemsFromTable(table,column,key)

    def getQuestionById(self,table,column,key):
        return self.getItemsFromTable(table,column,key)

    def getProductDataById(self,table,column,key):
        return self.getItemsFromTable(table,column,key)

    def getProductById(self,table,column,key):
        return self.getItemsFromTable(table,column,key)

    def getNoticeById(self,table,column,key):
        return self.getItemsFromTable(table,column,key)

    def getFeedbackById(self,table,column,key):
        return self.getItemsFromTable(table,column,key)


    #def advancedSearch(self):

    """Inserting data into tables"""
    def insertIntoUser(self, info):
        command = "INSERT INTO user VALUES({user_id},'{username}','{password}','{first_name}','{last_name}','{email}','{country}','{state}','{city}','{adress_1}','{adress_2}','{zip_code}','{contact_info}','{cell_number}',{session_id})".format(
            user_id=info["user_id"], username=info["username"], password=info["password"],
            first_name=info["first_name"], last_name=info["last_name"], email=info["email"], country=info["country"],
            state=info["state"], city=info["city"], adress_1=info["adress_1"], adress_2=info["adress_2"],
            zip_code=info["zip_code"], contact_info=info["contact_info"], cell_number=info["cell_number"],
            session_id=info["session_id"])
        mycursor.execute(command)
        mariadb_connection.commit()

    def insertIntoUserbid(self, info):
        command = "INSERT INTO userbid VALUES({current_bid_id},{user_id},{product_id})".format(
            current_bid_id = info["current_bid_id"], user_id = info["user_id"], product_id = info["product_id"]
        )
        mycursor.execute(command)
        mariadb_connection.commit()

    def insertIntoProduct(self,info):
        command = "INSERT INTO product VALUES({product_id},{user_id},{product_data_id},'{title}')".format(
            product_id=info["product_id"], user_id=info["user_id"], product_data_id=info["product_data_id"], title=info["title"]
        )
        mycursor.execute(command)
        mariadb_connection.commit()

    def insertIntoProductdata(self,info):
        command = "INSERT INTO productdata VALUES({product_data_id},'{desc}',{condition},'{country}', '{city}', {is_auction}, {price}, '{shipping_type}', {shipping_price}, {image}, {date_added}, {date_expires}, '{category}', '{subcategory}')".format(
            product_data_id=info["product_data_id"], desc=info["desc"], condition=info["contition"], country=info["country"],
            city=info["city"], is_auction=info["is_auction"], price=info["price"], shipping_type=info["shipping_type"],
            shipping_price=info["shipping_price"], image=info["image"], date_added=info["date_added"], date_expires=info["date_expires"],
            category=info["category"], subcategory=info["subcategory"]
        )
        mycursor.execute(command)
        mariadb_connection.commit()

    #def insertInto

if __name__ == "__main__":

    metod = databaseController()

    #print json.dumps(metod.getUserById("user","country","'romania'"),indent=4)

    hashinfo={
        "current_bid_id" : 1,
        "user_id" : 1,
        "product_id" : 1
    }

    metod.InsertIntoUserbid(hashinfo)

    #mycursor.execute('insert into user values(3,"GabiHartobanu","mancare","Hirtobanu","Gabriel","gabi@yahoo.com","romania","","iasi","ciurebesti1","ciurbesti2","111","contacti1","0753******",3)')
    #mariadb_connection.commit()
    #print mycursor.fetchall()
    #mycursor.execute('INSERT INTO userbid VALUES (1,1,1)')
    #mariadb_connection.commit()
