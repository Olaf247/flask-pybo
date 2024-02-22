# Created by user at 2024-02-14

import os

BASE_DIR = os.path.dirname(__file__)
#__file__:C:\projects\myproject\config.py
print(f'__file__:{__file__}')
#BASE_DIR:C:\projects\myproject
print(f'BASE_DIR:{BASE_DIR}')

#데이터 베이스 접속 주소
SQLALCHEMY_DATABASE_URI ='sqlite:///{}'.format(os.path.join(BASE_DIR,'pybo.db'))
#SQLAlchemy의 이벤트를 처리하는 옵션=False로 비활성화
SQLALCHEMY_TRACK_MODIFICATIONS = False

#SECRET_KEY : CSRF(cross-site request forgery)라는 웹사이트 취약점 공격방지,
# 폼으로 전송된 데이터가 실제 웹 페이지에서 작성된 데이터인지 판단해 주는 역할(웹위변조방지)
SECRET_KEY = "dev"
