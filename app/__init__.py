from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = 'Henry'

# 데이터베이스 설정
engine = create_engine('mysql+pymysql://root:Tmd%4078799858@localhost:3306/final_642', echo=False)
Session = sessionmaker(bind=engine)
db_session = Session()

# 뷰 임포트
from app import views
