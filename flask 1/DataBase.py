import  sqlite3, datetime
class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM posts'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: 
                return res
        except:
            #print ('Ошибка чтения из бд')
            return False
        return []
    
    def getJSON(self):
        sql = '''SELECT * FROM posts'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: 
                blocks_list = [dict(ix) for ix in res]
                return blocks_list
        except:
            #print ('Ошибка чтения из бд')
            return False
        return []

    def getTechnJSON(self):
        sql = '''SELECT * FROM technologies'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                blocks_list = [dict(ix) for ix in res]
                return blocks_list
        except:
            #print ('Ошибка чтения из бд')
            return False
        return []


    
    def addPost(self, title, content, user, status):
        try:
            today = datetime.datetime.today()
            tm = today.strftime("%d/%m/%Y")

            self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?, ?, ?)", (tm, title, content, status, user))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД" + str(e))
            return False
        return True
    
    def addTech(self, summary, content):
        try:
            self.__cur.execute("INSERT INTO technologies VALUES(NULL, ?, ?)", (summary, content))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления технологии в БД" + str(e))
            return False
        return True

    
    def updateStatus(self, title, content, status, id):
        try:
            self.__cur.execute(f"UPDATE posts SET title=?, content=?, status=? WHERE id=?", (title, content, status, id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД: " + str(e))
            return False
        return True
    
    def updateTechn(self, title, content, id):
        try:
            self.__cur.execute(f"UPDATE technologies SET summary=?, content=? WHERE id=?", (title, content, id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка обновления технологии в БД: " + str(e))
            return False
        return True
    

    def getPost(self, postId):
        try:
            self.__cur.execute(f"SELECT title, content FROM posts WHERE id = {postId} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            #print("Ошибка получения статьи из БД "+str(e))
            return False
        return (False, False)
    

    """ def getImage(self, postId):
        try:
            self.__cur.execute(f"SELECT title, content FROM posts WHERE id = {postId} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            #print("Ошибка получения статьи из БД "+str(e))
            return False
        return (False, False) """
 
    
    def addUser(self, name, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}' ")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким email уже существует")
                return False
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?)", (name, email, hpsw, 0))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД "+str(e))
            return False
        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользовательн не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения из БД "+str(e))
        return False
    
    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email= '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            
            return res 
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False
    

    def getAllUsers(self):
        try:
            self.__cur.execute(f"SELECT * FROM users")
            res = self.__cur.fetchall()
            if res:
                blocks_list = [dict(ix) for ix in res]
                return blocks_list
            
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False
    
    def getUserPostsJSON(self, userId):
        try:
            self.__cur.execute(f"SELECT created, title, content, status FROM posts WHERE author = {userId} ")
            res = self.__cur.fetchall()
            if res:
                blocks_list = [dict(ix) for ix in res]
                return blocks_list
        except sqlite3.Error as e:
            print(e)
            return False
        return ()