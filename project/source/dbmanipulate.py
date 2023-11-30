from pymysqlpool import ConnectionPool
import pymysql, datetime

dbconfig = {
    "host":'db-tech4impact-rsj.c8attu0agcw6.ap-northeast-2.rds.amazonaws.com',
    "user":'admin',
    "password":'tech4impact!',
    "db":'tech4impact',
    "charset":'utf8',
    "autocommit":True
}

pool= ConnectionPool(size=2, maxsize=3, pre_create_num=2, name='pool1',
                              **dbconfig)



# 연결 관리 함수 정의
def get_db_connection():
    connection = pool.get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    return connection, cursor
    
    # return pymysql.connect(
    #     host='db-tech4impact-rsj.c8attu0agcw6.ap-northeast-2.rds.amazonaws.com',
    #     user='admin',
    #     password='tech4impact!',
    #     db='tech4impact',
    #     charset='utf8',
    #     autocommit=True
    # )

def close_db_connection(connection, cursor):
    cursor.close()
    connection.close()

#안되면(에러시) None 반환 

#############################################
def team_get_all():
    conn, cur = get_db_connection()
    
    try:
        # 쿼리 실행
        query = "select * from Teams WHERE usable=1"
        cur.execute(query)
        res = cur.fetchall()
        for r in res:
            r['start_day'] = r['start_day'].strftime("%Y_%m_%d")
            r['end_day'] = r['end_day'].strftime("%Y_%m_%d")
        return res
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
        print("CLOSED")
#id, link, name, master_nickname, introduce
 
def team_get(Team_id: int):
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        query = "select * from Teams WHERE team_id = %s"
        cur.execute(query, Team_id)
        res = cur.fetchone()    
        return res
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)

def team_add(name, link, category, introduce, master_id, start_day, end_day): #id 도 받아야 할 것 같은데...
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        query = "INSERT INTO Teams(name, link, category, introduce, master_id, start_day, end_day) VALUE (%s, %s, %s, %s, %s, %s, %s)"
        cur.execute(query, (name, link, category, introduce, master_id, start_day, end_day))
        team_id = conn.insert_id()
        
        return True
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)

def team_delete(caller_id:int, Team_id:int):
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        query = "SELECT master_id from Teams WHERE team_id = %s"
        cur.execute(query, (Team_id))
        mid = cur.fetchone()['master_id'] #팀 마스터인지
        query = "SELECT is_manager FROM Users WHERE user_id = %s"
        cur.execute(query, (caller_id))
        is_manager = cur.fetchone()['is_manager'] #관리자 인지
        
        if is_manager or mid == caller_id : #팀 마스터이거나 관리자의 경우
            query = "UPDATE Teams SET usable=0 where team_id = %s"
            cur.execute(query, (Team_id))
        
            return True
        else: #권한이 없는 경우
            return False
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)

def team_user_applied():
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        query = "SELECT user_id, nickname, team_id, name AS team_name FROM Queue_User_Team JOIN Users USING(user_id) JOIN Teams USING(team_id) WHERE team_assigned = 0"
        cur.execute(query)
        res = cur.fetchall()
        return res
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
        
def team_user_withdrawn():
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        query = "SELECT user_id, nickname, team_id, name AS team_name FROM Queue_User_Team JOIN Users USING(user_id) JOIN Teams USING(team_id) WHERE team_assigned = 3"
        cur.execute(query)
        res = cur.fetchall()
        return res
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
        
def team_get_num():
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        query = "SELECT team_id, count(user_id) AS team_member_num FROM Relation_Team_User GROUP BY team_id;"
        cur.execute(query)
        res = cur.fetchall()
        return res
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)  


######################################
def user_get_all():
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        query = "select Users.*, team_id from Users LEFT JOIN Relation_Team_User Using(user_id)"
        cur.execute(query)
        res = cur.fetchall()
        for item in res:
            if item["team_id"] is None:
                item.update({"team_id": 0})
        return res
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)    

def user_get(Team_id: int):
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        query = "SELECT * FROM Users JOIN Relation_Team_User Using(user_id) WHERE team_id = %s"
        cur.execute(query, (Team_id))
        res = cur.fetchall()
        
        return res
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
        
def user_add(userid:str, password: str, user_name:str, nickname:str, email: str):
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        query = "SELECT login_id FROM Users where login_id = %s"
        cur.execute(query, (userid))
        if len(cur.fetchall()) > 0 : 
            print("There already exist user")
            return False 
    
        query = "INSERT INTO Users(login_id, password, user_name, nickname, email, is_manager) VALUE (%s, %s, %s, %s, %s, false)"
        cur.execute(query, (userid, password, user_name, nickname, email))
        query = "SELECT user_id From Users WHERE login_id = %s AND password=%s"
        cur.execute(query, (userid, password))
        res = cur.fetchone()
        return res
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
def user_delete(User_id: int):
    conn, cur = get_db_connection()
 
    try:

        cur.execute("DELETE FROM Relation_Team_User WHERE user_id = %s", User_id)
        cur.execute("DELETE FROM Relation_User_Mission WHERE user_id = %s", User_id)
        cur.execute("DELETE FROM Queue_User_Team WHERE user_id = %s", User_id)
        
        cur.execute("SELECT user_id from Users WHERE not user_id=%s", User_id)
        first_user = cur.fetchone()['user_id']
        cur.execute("UPDATE Teams SET master_id = %s WHERE master_id = %s", (first_user, User_id))
        
        # 쿼리 실행
        query = "DELETE FROM Users where user_id = %s"
        cur.execute(query, (User_id))
        return True
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
        
def user_makemanager(User_id: int):
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행

        query = "UPDATE Users SET is_manager = True WHERE user_id = %s"
        cur.execute(query, (User_id)) 
        return True
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
        

def user_todaymission(User_id: int, date: str):
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        query = """
                SELECT R.user_mission_id as user_mission_id, title, mission_type, submit_type, is_success, from_team
                FROM Relation_User_Mission as R
                JOIN Missions as M
                USING (mission_id)
                WHERE R.mission_date = %s AND R.user_id = %s
                """
                
        cur.execute(query, (date, User_id))
        res = cur.fetchall()
        return res
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
        
def user_setsuccess(User_Mission_id: int):
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행

        query = "UPDATE Relation_User_Mission SET is_success = 1-is_success WHERE user_mission_id = %s"
        cur.execute(query, (User_Mission_id)) 
        return True 
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)

def mission_get( date: str):
    conn, cur = get_db_connection()
    try:
        # 쿼리 실행

        query = "select Relation_User_Mission.*, title, mission_type, submit_type from Relation_User_Mission JOIN Missions USING(mission_id) WHERE mission_date = %s ORDER BY user_mission_id"
        cur.execute(query, ( date)) 
        res = cur.fetchall()
        return res
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
        
def mission_get_team( date: str, teamId : int):
    conn, cur = get_db_connection()
    try:
        # 쿼리 실행

        query = "select Relation_User_Mission.*, title, mission_type, submit_type, nickname from Relation_User_Mission JOIN Missions USING(mission_id) JOIN Relation_Team_User using(user_id) JOIN Users USING(user_id) WHERE mission_date = %s AND team_id=%s ORDER BY user_mission_id"
        cur.execute(query, ( date , teamId)) 
        res = cur.fetchall()
        return res
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
        
        
def user_mission_add(title:str, missionType:str, mission_date:str, user_id:int):
    conn, cur = get_db_connection()
    try:
        # 쿼리 실행
        query = "INSERT INTO Missions(title, mission_type, submit_type) VALUES(%s, %s, 'check')"
        cur.execute(query, (title, missionType))
        query = "SELECT mission_id FROM Missions WHERE title = %s AND mission_type = %s ORDER BY mission_id DESC"
        cur.execute(query, (title, missionType))
        mission_id = cur.fetchone()['mission_id']
        print(mission_id)
        
        query = "INSERT INTO Relation_User_Mission(mission_date, mission_id, user_id, is_success, from_team) VALUES(%s, %s, %s, false, false)"
        cur.execute(query, (mission_date, mission_id, user_id))
        mid = conn.insert_id()
        cur.execute("SELECT * FROM Relation_User_Mission WHERE user_mission_id = %s", (mid))
        res = cur.fetchone()
        res['mission_date'] = res['mission_date'].strftime("%Y_%m_%d")
        return res
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)

def user_mission_delete(user_mission_id):
    conn, cur = get_db_connection()
    try:
        # 쿼리 실행

        query = "DELETE FROM Relation_User_Mission WHERE user_mission_id = %s"
        cur.execute(query, (user_mission_id)) 

        return True
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)

def user_assign_team(userId:str, teamId:str, acceptOrNot:int):
    conn, cur = get_db_connection()
    try:
        # 쿼리 실행
        if acceptOrNot:
            cur.execute(f"SELECT * FROM Relation_Team_User WHERE user_id = '{userId}'")
            existing_row = cur.fetchone()
            if existing_row:
                # 결과가 존재하면 해당 행의 team_id를 Y로 업데이트
                cur.execute(f"UPDATE Relation_Team_User SET team_id = '{teamId}' WHERE user_id = '{userId}'")
            else:
                # 결과가 없으면 새로운 행 추가
                cur.execute(f"INSERT INTO Relation_Team_User (user_id, team_id) VALUES ('{userId}', '{teamId}')")
        
        cur.execute(f"UPDATE Queue_User_Team SET team_assigned = {2 - acceptOrNot}  WHERE user_id = '{userId}' AND team_id = '{teamId}'") 
        return True
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
        
def user_request_team(userId, teamId):
    conn, cur = get_db_connection()
    try:
        # 쿼리 실행
        query = "SELECT user_id, team_id FROM Queue_User_Team WHERE user_id=%s AND team_id = %s AND team_assigned=0"
        cur.execute(query, (userId, teamId))
        res = cur.fetchone()
        if res is None:
            query = "INSERT INTO Queue_User_Team (user_id, team_id, team_assigned) VALUES (%s, %s, 0);"
            cur.execute(query, (userId, teamId))
            query = "SELECT user_id, team_id FROM Queue_User_Team WHERE user_id=%s AND team_id = %s AND team_assigned=0"
            cur.execute(query, (userId, teamId))
            res = cur.fetchone()
        return res
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)

def user_withdraw_team(userId, teamId): # 해야 함
    conn, cur = get_db_connection()
    try:
        # 쿼리 실행
        query = "SELECT user_id, team_id FROM Queue_User_Team WHERE user_id=%s AND team_id = %s AND team_assigned=3"
        cur.execute(query, (userId, teamId))
        res = cur.fetchone()
        if res is None:
            query = "INSERT INTO Queue_User_Team (user_id, team_id, team_assigned) VALUES (%s, %s, 3);"
            cur.execute(query, (userId, teamId))
            query = "SELECT user_id, team_id FROM Queue_User_Team WHERE user_id=%s AND team_id = %s AND team_assigned=3"
            cur.execute(query, (userId, teamId))
            res = cur.fetchone()
        return res
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)

def user_erase_team(userId:str, teamId:str, acceptOrNot:int):
    conn, cur = get_db_connection()
    try:
        # 쿼리 실행
        if acceptOrNot:
            cur.execute(f"SELECT * FROM Relation_Team_User WHERE user_id = '{userId}' AND team_id = '{teamId}'")
            existing_row = cur.fetchone()
            if existing_row:
                # 결과가 존재하면 해당 행의 team_id를 Y로 업데이트
                cur.execute(f"DELETE FROM Relation_Team_User WHERE user_id = '{userId}' AND team_id = '{teamId}'")
            
        cur.execute(f"UPDATE Queue_User_Team SET team_assigned = {2 - acceptOrNot}  WHERE user_id = '{userId}' AND team_id = '{teamId}'") 
        return True
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)

def user_login(loginId: str, password:str):
    conn, cur = get_db_connection()
    try:
        # 쿼리 실행
        query = "SELECT * FROM Users WHERE login_id = %s AND password = %s"
        cur.execute(query, (loginId, password))
        res = cur.fetchone()
        
        return res
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
        
def user_get_info(userId : int):
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        query = "select * from Users WHERE user_id = %s"
        cur.execute(query, (userId))
        res = cur.fetchone() 
        res['team_id'] = user_if_has_team(userId)['team_id']
        return res
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)   

def user_if_has_team(user_id:int):
    conn, cur = get_db_connection()
 
    try:
        query = "select team_id from Relation_Team_User WHERE user_id=%s"
        cur.execute(query, (user_id))
        team_id = cur.fetchone()
        res = {}
        res['team_id'] = team_id['team_id'] if team_id is not None else 0 
        return res
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)   

def user_change_info(userid:int, password: str, user_name:str, nickname:str, email: str, teamid:int): 
    conn, cur = get_db_connection()
    try:
        # 쿼리 실행
        query = """
        UPDATE Users
SET 
    password = %s,
    user_name = %s,
    nickname = %s,
    email = %s
WHERE
    user_id = %s
        """
        cur.execute(query, (password, user_name, nickname, email, userid))
        if teamid != 0:user_set_team(userid, teamid)
        res = user_get_info(userid)
        
        return res
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
        
def user_set_team(user_id:int, team_id: int):
    conn, cur = get_db_connection()
    try:
        # 쿼리 실행
        query = 'SELECT * from Relation_Team_User WHERE user_id = %s'
        cur.execute(query, (user_id))
        TEAM_EXIST = cur.fetchone()
        if TEAM_EXIST is None:
            #팀 없음
            query = "INSERT INTO Relation_Team_User(team_id, user_id) VALUES(%s, %s)"
        else:
            query = "UPDATE Relation_Team_User SET team_id = %s WHERE user_id=%s"
        cur.execute(query, (team_id, user_id))

        query = 'SELECT user_id, team_id from Relation_Team_User WHERE user_id = %s'
        cur.execute(query, user_id)
        res = cur.fetchone()
        return res
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)    
    
    
def mission_add(title: str, mission_type: str):
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        query = "INSERT INTO Missions(title, mission_type, submit_type) VALUES(%s, %s, 'check')"
        cur.execute(query, (title, mission_type))
        query = "SELECT mission_id FROM Missions WHERE title = %s AND mission_type = %s ORDER BY mission_id DESC"
        cur.execute(query, (title, mission_type))
        res = cur.fetchone()
        return res
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)

def mission_assign(date: str, user_id : int, mission_id : int):
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        query = "INSERT INTO Relation_User_Mission(mission_date, mission_id, user_id, is_success, from_team) VALUES(%s, %s, %s, false, true)"
        cur.execute(query, (date, mission_id, user_id))
        mid = conn.insert_id()
        cur.execute("SELECT * FROM Relation_User_Mission WHERE user_mission_id = %s", (mid))
        res = cur.fetchone()
        res['mission_date'] = res['mission_date'].strftime("%Y_%m_%d")
        return res
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)

def mission_delete(mission_id: int):
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        query = "DELETE FROM Missions WHERE mission_id = %s"
        cur.execute(query, (mission_id))
        return True
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)

def mission_assign_team(date:str, team_id:int, mission_id : int):
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        query = "SELECT user_id FROM Users JOIN Relation_Team_User USING(user_id) WHERE team_id = %s"
        cur.execute(query, (team_id,))
        user_ids = cur.fetchall()
        user_ids = [x['user_id'] for x in user_ids]
        query = "INSERT INTO Relation_User_Mission(mission_date, user_id, mission_id, is_success, from_team) VALUES(%s, %s, %s, 0, 1)"
        values = [ [date, x, mission_id] for x in user_ids]
        print(values)
        cur.executemany(query, values)
        
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
    return True

def mission_all():
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        query = "SELECT * FROM Missions"
        cur.execute(query)
        res = cur.fetchall()
        return res
        
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
    return True

def mission_assigned_all():
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        query = "SELECT * FROM Relation_User_Mission"
        cur.execute(query)
        res = cur.fetchall()
        return res
        
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
    return True


def stats_user_daily(user_id:int, date:str):
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        query = """
                select mission_date, count(*) as num_mission, sum(is_success) as num_success , ROUND(sum(is_success) / count(*) * 100) as percentage
                from Relation_User_Mission
                WHERE user_id=%s AND mission_date = %s
                GROUP BY mission_date"""
        cur.execute(query, (user_id, date))
        res = cur.fetchone()
        if res==None:
            res = {'mission_date':date, 'num_mission':0, 'num_success':0, 'percentage':0 }
        return res
        
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
    return True

def stats_user_month(user_id:int, date:str):
    #미완성
    conn, cur = get_db_connection()

    try:
        res = []
        date_obj = datetime.datetime.strptime(date, "%Y_%m_%d")
        start_date = datetime.date(date_obj.year, date_obj.month, 1)
        end_date = date_obj.date()

        date_range = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]
        query = """
    SELECT
        mission_date,
        COUNT(*) AS num_mission,
        SUM(is_success) AS num_success,
        ROUND(SUM(is_success) / COUNT(*) * 100) AS percentage
    FROM
        Relation_User_Mission
    WHERE
        user_id = %s
        AND mission_date = %s
    GROUP BY
        mission_date
"""

        
        for date in date_range:
            cur.execute(query, (user_id, date))
            result = cur.fetchone()
            res.append( int(result['percentage']) if result else 0 )
                
        
        return res
        
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
    return True

def stats_team_daily(team_id:int, date:str): #userid, user nickname 추가하기
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        cur.execute("SELECT user_id from Relation_Team_User WHERE team_id = %s", team_id)
        user_ids = cur.fetchall()
        user_ids = [x['user_id'] for x in user_ids]
        
        res = []
        for user_id in user_ids:
            midres = stats_user_daily(user_id, date)
            cur.execute("SELECT nickname FROM Users WHERE user_id = %s", user_id)
            nickname = cur.fetchone()['nickname']
            midres['user_id'] = user_id
            midres['nickname'] = nickname
            res.append(midres)
        return res
        
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
    return True    

    

def stats_all_daily(date:str): #userid, user nickname 추가하기
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        cur.execute("SELECT user_id from Users")
        user_ids = cur.fetchall()
        user_ids = [x['user_id'] for x in user_ids]
        
        res = []
        for user_id in user_ids:
            midres = stats_user_daily(user_id, date)
            cur.execute("SELECT nickname FROM Users WHERE user_id = %s", user_id)
            nickname = cur.fetchone()['nickname']
            midres['user_id'] = user_id
            midres['nickname'] = nickname
            res.append(midres)
        return res
        
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
    return True    

def stats_all_month( date:str):
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        start_date = date 
        query = """
SELECT Q.*, nickname
from (SELECT user_id, count(*) as num_mission, sum(is_success) AS num_success, ROUND(100 * sum(is_success) / count(*)) as percentage
FROM Relation_User_Mission
WHERE mission_date BETWEEN %s AND %s
GROUP BY user_id) AS Q
JOIN Users USING(user_id)
    """
        cur.execute(query, (date[0:8]+"01", date))
        res = cur.fetchall()
        return res
        
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
    return True   
    
def stats_all_team_sum_daily(date:str):
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        start_date = date 
        
        query = """
SELECT Q.*, name as nickname

FROM (SELECT team_id, count(*) as num_mission, sum(is_success) AS num_success,  ROUND(100 * sum(is_success) / count(*)) as percentage
FROM Relation_User_Mission JOIN Relation_Team_User USING(user_id)
WHERE mission_date = %s
GROUP BY team_id) as Q
JOIN Teams USING(team_id)
"""
        cur.execute(query, (date))
        res = cur.fetchall()
        if res == () : res = []
        teams = [] if res == () else [x['team_id'] for x in res]
        all_teams = team_get_all()
        all_teams = [[x['team_id'], x['name']] for x in all_teams]
        for team_id, team_nickname in all_teams:
            if team_id in teams: continue
            res.append({ "team_id" : team_id, "num_mission" : 0, "num_success" : 0, "percentage" : 0, 'nickname': team_nickname})
        return res
        
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
    return True  


def stats_all_team_sum_month(date:str):
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 실행
        start_date = date 
        
        query = """
SELECT Q.*, name as nickname FROM (
SELECT team_id, count(*) as num_mission, sum(is_success) AS num_success,  ROUND(100 * sum(is_success) / count(*)) as percentage
FROM Relation_User_Mission JOIN Relation_Team_User USING(user_id)
WHERE mission_date BETWEEN %s AND %s
GROUP BY team_id
) AS Q
JOIN Teams USING(team_id)
"""
        cur.execute(query, (date[0:8]+"01", date))
        res = cur.fetchall()
        if res == () : res = []
        teams = [] if res is None else [x['team_id'] for x in res]
        all_teams = team_get_all()
        all_teams = [[x['team_id'], x['name']] for x in all_teams]
        for team_id, team_nickname in all_teams:
            if team_id in teams: continue
            res.append({ "team_id" : team_id, "num_mission" : 0, "num_success" : 0, "percentage" : 0, 'nickname': team_nickname})
        return res
        
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
    return True  

import random
    
if __name__ == "__main__" :
    missions = mission_assigned_all()
    print(stats_all_month('2023-11-26'))
    print(stats_all_team_sum_daily('2023-10-26'))
    print(stats_all_team_sum_month('2023-10-26'))
    print(mission_get_team('2023-11-27', 28))
    #print(user_add("login123", "pass", "김익명", "Nick", "email@str"))
    # teams = team_get_all()
    # teams = [x['team_id'] for x in teams][:2]
    
    
    
    # users = user_get_all()
    # users = [x['user_id'] for x in users]
    
    # for user in users:
    #     random_team = random.choice(teams)
    #     print(user, random_team)
    #     user_set_team(user, random_team)
    
    #print(user_change_info(53,'1','1','1', '1', 1))
    #mission_add("일어나서 공복에 물 1컵 마시기", "시도해력")
    #print(mission_add("일어나서 공복에 물 1컵 마시기", "시도해력"))
    #print(user_add("userid2", "password: str", "user_name:str", "nickname:str", "email: str"))
    #print(user_mission_add("title:str", missionType:str, mission_date:str, user_id:int))
    # http://13.124.69.102:5000/team/add/?name=23&link=2&category=2&introduce=&masterId=2&startDate=2023-10-04&endDate=2023-10-25