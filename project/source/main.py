from typing import Union
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import dbmanipulate as DB

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "https://localhost",
        "http://localhost:3000",
        "https://localhost:3000",
        "http://localhost:8080",
        "https://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/index.html", response_class=HTMLResponse)
async def show_index_html():
    return """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>tech for impact</title>
</head>
<body>

    <h1>제목</h1>
    <h3>테스트 페이지. 나중에 관리자 페이지 그냥 여기다 얹고 리소스만 버킷으로 빼도..</h3>

</body>
</html>
            """

# ///// team /////

@app.get("/team/all/")
def team_get_all():
    try:
        qr = DB.team_get_all()
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/team/get/")
def team_get(teamId: int):
    try:
        qr = DB.team_get(teamId)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/team/add/")
def team_add(name:str, link:str, category:str, introduce:str, masterId:str, startDay:str, endDay:str):
    try:
        qr = DB.team_add(name, link, category, introduce, masterId, startDay, endDay)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/team/delete/")
def team_delete(callerId:int, teamId: int):
    try:
        qr = DB.team_delete(callerId, teamId)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/team/getNum/")
def team_get_num():
    try:
        qr = DB.team_get_num()
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/team/userApplied")
def team_get_num():
    try:
        qr = DB.team_user_applied()
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/team/userWithdrawn")
def team_user_withdrawn():
    try:
        qr = DB.team_user_withdrawn()
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

# ///// user /////

@app.get("/user/all/")
def user_get_all():
    try:
        qr = DB.user_get_all()
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/user/get/")
def user_get(teamId: int):
    try:
        qr = DB.user_get(teamId)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/user/add/")
def user_add(login_id:str, password: str, user_name:str, nickname:str, email: str):
    try:
        qr = DB.user_add(login_id, password, user_name, nickname, email)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/user/delete/")
def user_delete(userId: int):
    try:
        qr = DB.user_delete(userId)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/user/makeManager/")
def user_makemanager(userId: int):
    try:
        qr = DB.user_makemanager(userId)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

#아이디 말고 다른 것(타입, 텍스트)도 들어 가게 하기
@app.get("/user/todayMission/")
def user_todaymission(userId: int, date: str):    
    try:
        qr = DB.user_todaymission(userId, date)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/user/setSuccess/")
def user_setsuccess(userMissionId: int):
    try:
        qr = DB.user_setsuccess(userMissionId)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/user/assignTeam")
def user_assign_team(userId: int, teamId: int, acceptOrNot:int):
    try:
        qr = DB.user_assign_team(userId, teamId, acceptOrNot)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }    

@app.get("/user/requestTeam")
def user_request_team(userId: int, teamId: int):
    try:
        qr = DB.user_request_team(userId, teamId)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }    

@app.get("/user/eraseTeam")
def user_assign_team(userId: int, teamId: int, acceptOrNot:int):
    try:
        qr = DB.user_erase_team(userId, teamId, acceptOrNot)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }    

@app.get("/user/withdrawTeam")
def user_withdraw_team(userId: int, teamId: int):
    try:
        qr = DB.user_withdraw_team(userId, teamId)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }   

@app.get("/user/login")
def user_login(loginId: str, password: str ):
    try:
        qr = DB.user_login(loginId, password)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/user/getInfo")
def user_get_info(userId : int ):
    try:
        qr = DB.user_get_info(userId)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/user/changeInfo")
def user_change_info(userId:int, password: str, user_name:str, nickname:str, email: str, teamId:int):
    try:
        qr = DB.user_change_info(userId, password, user_name, nickname, email, teamId)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/user/ifHasTeam")
def user_if_has_team(userId:int):
    try:
        qr = DB.user_if_has_team(userId)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }


@app.get("/mission/get")
def mission_get(date: str):
    try:
        qr = DB.mission_get(date)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/mission/getTeam")        
def mission_get_team( date: str, teamId : int):
    try:
        qr = DB.mission_get_team(date, teamId)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/user/mission/add")
def user_mission_add(title: str, missionType: str, date:str, userId:int):
    try:
        qr = DB.user_mission_add(title, missionType, date, userId)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/user/mission/delete")
def user_mission_add(user_mission_id):
    try:
        qr = DB.user_mission_delete(user_mission_id)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/mission/add")
def mission_add(title: str, missionType: str):
    try:
        qr = DB.mission_add(title, missionType)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/mission/assign")
def mission_assign(date: str, userId : int, missionId : int):
    try:
        qr = DB.mission_assign(date, userId, missionId)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/mission/delete")
def mission_delete(missionId: int):
    try:
        qr = DB.mission_delete(missionId)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/mission/assign_team")
def mission_assign_team(date:str, teamId:int, missionId : int):
    try:
        qr = DB.mission_assign_team(date, teamId, missionId)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }
        
@app.get("/mission/all")
def mission_all():
    try:
        qr = DB.mission_all()
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }
        
@app.get("/stats/userDaily")
def stats_user_daily(user_id:int, date:str):
    try:
        qr = DB.stats_user_daily(user_id, date)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }
        
@app.get("/stats/userMonth")
def stats_user_month(userId:int, date:str):
    try:
        qr = DB.stats_user_month(userId, date)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }
   
@app.get("/stats/teamDaily")
def stats_team_daily(team_id:int, date:str):
    try:
        qr = DB.stats_team_daily(team_id, date)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }
     
@app.get("/stats/allDaily")
def stats_all_daily(date:str):
    try:
        qr = DB.stats_all_daily(date)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }
    
@app.get("/stats/allMonth")
def stats_all_month(date:str):
    try:
        qr = DB.stats_all_month(date)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }


@app.get("/stats/allTeamSumDaily")
def stats_all_team_sum_daily(date:str):
    try:
        qr = DB.stats_all_team_sum_daily(date)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }

@app.get("/stats/allTeamSumMonth")
def stats_all_team_sum_month(date:str):
    try:
        qr = DB.stats_all_team_sum_month(date)
        print(qr)
        if qr == None:
            return {
                "status":"not found",
                "data": {}
            }
        else:
            return {
                "status":"ok",
                "data":
                qr
            }
    except:
        return {
            "status":"Error Occured",
            "data": {}
        }