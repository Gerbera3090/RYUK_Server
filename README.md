# RYUK_Server

## 테크포임팩트 력습지 조 서버 프로젝트
### 개발자
* 송민우 - 전산학부, 20학번 : 서버 환경 구축 및 라우팅 환경 구축
* 권혁원 - 전산학부, 21학번 : DB 환경 구축 및 API 작성

### 사용 언어
+ 서버 : AWS EC2
+ Database : AWS RDB + MariaDB 10.6
+ Code : Python, FastAPI
+ 사용한 라이브러리 : pymysql,pymysqlpool

------
## 서버 구동 방법

### 서버 켜기
* project 폴더로 진입
* 가상 환경 활성화

  source bin/activate

* source 폴더 진입
* 서버 활성화

  source server.sh;run

### 서버 재시작

* 위 과정 반복
* 서버 끄기
  source server.sh;kill
* 서버 활성화
  source server.sh;run

------
## 파일 설명

### DB_MAKE_QUERIES.txt
DB를 정의하는 DDL을 작성한 파일 

안에 있는 DDL을 mysql browser 등을 이용하여 DB 초기 설정 가능

![image](https://github.com/Gerbera3090/RYUK_Server/assets/52480724/1805c404-adaa-4e3c-8384-69ed5c9fb34e)


### dbmanipulate.py

Mysql DB에 접근하여 정보를 처리하는 파일

#### 함수 작성 템플릿
```
def API_FUNCTION():
    conn, cur = get_db_connection()
 
    try:
        # 쿼리 및 이후 필요한 작업 수행
        query = "QUERY"
        cur.execute(query)
        RETURN_VALUE = cur.fetchall()
        return RETURN_VALUE
    finally:
        # 연결 닫기
        close_db_connection(conn, cur)
```

의 형태로 작성함.

### main.py

Fast API를 이용하여 라우팅을 처리하는 파일

#### 라우팅 받기

#### 함수 작성 템플릿
```
@app.get("GET_하는_주소")
def FUNCTION_NAME(REQUEST_INPUTS):
    try:
        qr = DB.API_FUNCTION(REQUEST_INPUTS)
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
```


답변은 항상 
```
{
  'status' : STATUS,
  'data' : DATA
}
```
의 형태로 반환

status 가 가질 수 있는 값은 'ok', 'not found', "Error Occured" 의 세 가지
- "Error Occured" : API 내부 및 라우팅 과정에서 오류 발생
- 'ok' : 존재하는 값에 대한 request 가 잘 들어왔고, 값을 잘 반환함
- 'not found' : 문법상 오류는 없으나 없는 값에 대한 request가 들어옴.





