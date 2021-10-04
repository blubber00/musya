import pymysql
from settings import host_mysql1, user_mysql1, password_mysql1, db_mysql1

def connect_msql():
    db = pymysql.Connection(
        host = host_mysql1,
        user = user_mysql1,
        password = password_mysql1,
        db = db_mysql1,
        port=3306
    )
    return(db)

def cmd_start(message):
    nickname = message['from']['username']
    if check_account(nickname) == False:
        new_id = int(get_last_count()) + 1
        sql = f"""
        INSERT INTO USERS(
            ID, COUNT, USER_NICKNAME, KOSTI_SET
        ) 
        VALUES (
            '{new_id}', '1500', '{nickname}', '0'
        )
        """
        db = connect_msql()
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print(e)
        db.close()
        return(True)
    else:
        return(True)

def get_last_count():
    sql = """
    SELECT COUNT(*) FROM USERS
    """
    db = connect_msql()
    cursor = db.cursor()
    try:
        cursor.execute(sql)
    except Exception as e:
        print(e)
    result = cursor.fetchall()[0][0]
    db.close()
    return(result)
        
def check_account(nickname):
    sql = f"""
    SELECT * FROM USERS
    WHERE USER_NICKNAME='{nickname}'
    """
    db = connect_msql()
    cursor = db.cursor()
    try:
        cursor.execute(sql)
    except Exception as e:
        print (e)
    results = cursor.fetchall()
    db.close()
    if len(results) == 0:
        return False
    else:
        return True

def get_count(nickname):
    sql = f"""
    SELECT COUNT FROM USERS 
    WHERE USER_NICKNAME='{nickname}'
    """
    db = connect_msql()
    cursor = db.cursor()
    try:
        cursor.execute(sql)
    except Exception as e:
        print (e)
    result = str(cursor.fetchall()[0][0])
    db.close()
    return(result)

def get_id(nickname):
    sql = f"""
    SELECT ID FROM USERS 
    WHERE USER_NICKNAME='{nickname}'
    """
    db = connect_msql()
    cursor = db.cursor()
    try:
        cursor.execute(sql)
    except Exception as e:
        print (e)
    result = str(cursor.fetchall()[0][0])
    db.close()
    return(result)

def get_kosti_set(nickname):
    sql = f"""
    SELECT KOSTI_SET FROM USERS 
    WHERE USER_NICKNAME='{nickname}'
    """
    db = connect_msql()
    cursor = db.cursor()
    try:
        cursor.execute(sql)
    except Exception as e:
        print (e)
    result = str(cursor.fetchall()[0][0])
    db.close()
    return(result)

def kosti_set_price(nickname, count):
    sql = f"""
    UPDATE USERS SET KOSTI_SET='{count}' WHERE USER_NICKNAME='{nickname}'
    """
    db = connect_msql()
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
    return True

def set_new_count(nickname, count):
    sql = f"""
    UPDATE USERS SET COUNT='{count}' WHERE USER_NICKNAME='{nickname}'
    """
    db = connect_msql()
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
    return True

def test():
    sql = """
    INSERT INTO USERS(
        ID, COUNT
    ) 
    VALUES (
        '0', '7500'
    )
    """
    db = connect_msql()
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        print('Sussefull !!!')
    except Exception as e:
        print(e)

def test2():
    sql = """
    SELECT * FROM USERS
    """
    db = connect_msql()
    cursor = db.cursor()
    try:
        cursor.execute(sql)
    except Exception as e:
        print (e)
    results = cursor.fetchall()
    print(results[1])
