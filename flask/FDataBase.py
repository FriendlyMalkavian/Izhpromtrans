import sqlite3

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
    
    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []
    
    def getStations(self, alias): 
        try:
            self.__cur.execute(f"SELECT StationId, StationName, url FROM stations WHERE StationId = '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            if res: 
                return res
        except sqlite3.Error as e:
            print("Ошибка чтения из БД"+str(e))

        return (False, False)

    def stations(self, StationName, url):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM stations WHERE StationName LIKE '{StationName}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Такая станция уже существует")
                return False
            self.__cur.execute("INSERT INTO stations VALUES(NULL, ?, ?)", (StationName, url))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления станции в Базу Данных" +str(e))
            return False
        return True
    
    def getStationAnonce(self):
        try:
            self.__cur.execute(f"SELECT StationId, StationName, url FROM stations ORDER BY StationName")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения станции из БД"+str(e))
        
        return[]
    
    def propertyObjects(self, ObjectName):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM propertyObjects WHERE ObjectName LIKE '{ObjectName}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Такой объект уже существует")
                return False
            self.__cur.execute("INSERT INTO propertyObjects VALUES(NULL, ?)", tuple([ObjectName]))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления станции в Базу Данных" +str(e))
            return False
        return True
    
    def certificates(self, RegistrationNumber, PathLength, CadastralNumber, StationId):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM certificates WHERE RegistrationNumber LIKE '{RegistrationNumber}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Такой сертификат уже существует")
                return False
            self.__cur.execute("INSERT INTO certificates VALUES(NULL, ?, ?, ?, ?)", (RegistrationNumber, PathLength, CadastralNumber, StationId ))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления станции в Базу Данных" +str(e))
            return False
        return True
    
    def objectsInCertificates(self, CertificateId, ObjectId, StationId):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM objectsInCertificate WHERE ObjectId LIKE '{ObjectId}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Такой объект уже прикреплен к сертификату")
                return False
            self.__cur.execute("INSERT INTO objectsInCertificate VALUES(?, ?, ?)", (CertificateId, ObjectId, StationId))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления станции в Базу Данных" +str(e))
            return False
        return True
    
    def getCertificateAnonce(self):
        try:
            self.__cur.execute(f"SELECT CertificateId, StationId, RegistrationNumber FROM certificates")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения станции из БД"+str(e))
        return[]
    
    def getObjectAnonce(self):
        try:
            self.__cur.execute(f"SELECT ObjectId, ObjectName FROM propertyObjects ORDER BY ObjectId")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения станции из БД"+str(e))
        
        return[]
    
    def getObjectInCertificatesAnonce(self):
        try:
            self.__cur.execute(f"SELECT CertificateId, ObjectId, StationId FROM objectsInCertificate ORDER BY StationId")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения станции из БД"+str(e))
        
        return[]
    
    def tenants(self, TenantName):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM tenants WHERE TenantName LIKE '{TenantName}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Такой арендатор уже существует")
                return False
            self.__cur.execute("INSERT INTO tenants VALUES(NULL, ?)", tuple([TenantName]))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления арендатора в Базу Данных" +str(e))
            return False
        return True
    
    def getTenantAnonce(self):
        try:
            self.__cur.execute(f"SELECT TenantId, TenantName FROM tenants ORDER BY TenantId")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения арендаторов из БД"+str(e))
        
        return[]
    
    def rent(self, ContractNumber, RentPricePM, TenantId):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM rent WHERE ContractNumber LIKE '{ContractNumber}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Такой Договор уже существует")
                return False
            self.__cur.execute("INSERT INTO rent VALUES(NULL, ?, ?, ?)", (ContractNumber, RentPricePM, TenantId ))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления договора в Базу Данных" +str(e))
            return False
        return True
    
    def getRentAnonce(self):
        try:
            self.__cur.execute(f"SELECT RentId, ContractNumber, RentPricePM, TenantId FROM rent ORDER BY RentId")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения договоров из БД"+str(e))
    
        return[]
    
    def rentalObjects(self, RentId, ObjectId):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM rentalObjects WHERE ObjectId LIKE '{ObjectId}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Такой объект уже прикреплен к Договору")
                return False
            self.__cur.execute("INSERT INTO rentalObjects VALUES( ?, ?)", (RentId, ObjectId))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления станции в Базу Данных" +str(e))
            return False
        return True
    
    def getRentalObjectsAnonce(self):
        try:
            self.__cur.execute(f"SELECT RentId, ObjectId FROM rentalObjects ORDER BY RentId")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения Договоров из БД"+str(e))
        
        return[]