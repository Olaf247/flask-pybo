from flask import Blueprint, url_for
from werkzeug.utils import redirect

#__name__ : main_views.py
bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_pybo():
    return "<p>Hello, world!</p>"

# @bp.route('/detail/<int:question_id>/')
# def detail(question_id):
#     print(f'question_id:{question_id}')
#     #단건 조회
#     question = Question.query.get_or_404(question_id)
#     print(f'question:{question}')
#
#     return render_template('question/question_detail.html', question=question)
#
# @bp.route('/')
# def index():
#     #질문 목록을 날짜 역순으로 출력
#     question_list = Question.query.order_by(Question.create_date.desc())
#     '''
#     '''
#     print(f'question_list:{question_list}')
#
#     # '<p> Index <p>'/화면으로, question_list 데이터 전달
#     return render_template('question/question_list.html', question_list=question_list)

@bp.route('/')
def index():
    #redirect(URL) : URL로 페이지 이동
    #url_for(라우팅함수명) : 라우팅 함수에 매핑되어 있는 URL return
    print("-"*50)
    print(f'url_for(question_list):{url_for('question._list')}')
    print("-" * 50)
    return redirect(url_for('question._list'))