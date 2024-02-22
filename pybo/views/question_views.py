from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from pybo.forms import QuestionForm, AnswerForm
from pybo.models import Question
from .answer_views import login_required
from .. import db

bp = Blueprint('question', __name__, url_prefix='/question')

#순서가 @bp.route 뒤에 @login_required 위치. 그렇지 않으면 정상동작하지 않음
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = QuestionForm()

    print(f'create, request:{request.method}')
    print(f'form.validate_on_submit:{form.validate_on_submit()}')
    #request method가 post이고 form이 submit()이면
    # and form.validate_on_submit()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, contents=form.contents.data, create_date=datetime.now(), user=g.user)

        db.session.add(question)
        db.session.commit()

        print(f'main.index:{url_for('main.index')}')
        return redirect(url_for ('main.index'))

    return render_template('question/question_form.html', form=form)

#/question/detail/1
@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()

    print(f'question_id:{question_id}')
    #단건 조회
    question = Question.query.get_or_404(question_id)
    print(f'question:{question}')

    return render_template('question/question_detail.html', question=question, form=form)

#/question/list
#list : 파이썬 예약어
@bp.route('/list')
def _list():
    #질문 목록을 날짜 역순으로 출력
    question_list = Question.query.order_by(Question.create_date.desc())

    #paging : http://127.0.0.1:5000/question/list?page=1
    page = request.args.get('page', type=int, default=1)
    print(f'page:{page}')
    question_list = question_list.paginate(page=page, per_page=10)#상수 개념이 없고 관례적으로 사용

    '''
    question_list:
    SELECT question.id AS question_id, question.subject AS question_subject, 
            question.contents AS question_contents, question.create_date AS question_create_date
    FROM question ORDER BY question.create_date DESC
    '''
    print(f'question_list:{question_list}')

    # '<p> Index <p>'/화면으로, question_list 데이터 전달
    return render_template('question/question_list.html', question_list=question_list)

#수정 : question_form.html 같이 사용
@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    print('-'*50)
    print(f'question_id:{question_id}')
    print(f'request.method:{request.method}')
    print('-' * 50)

    question = Question.query.get_or_404(question_id)
    #수정 권한 체크
    if g.user != question.user:
        flash('수정 권한 없음')
        return redirect( url_for('question.detail', question_id=question_id) )

    if request.method == 'POST': #POST
        form = QuestionForm()
        if form.validate_on_submit():
            #수정 : form변수 들어 있는 데이터를 question객체에 update 역할
            form.populate_obj(question) #화면에서 들어오는 질문(제목, 내용) update
            question.modify_date = datetime.now() #수정일시
            print(f'question:{question}')

            db.session.commit()
            return redirect( url_for('question.detail', question_id=question_id)) #POST

    else: #GET
        form = QuestionForm(obj=question)

    return render_template('question/question_form.html', form=form)

#삭제 : delete
@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id) #question_id에 해당하는 데이터 단건 조회

    #권한 : 글쓴이만 삭제 가능
    if g.user != question.user:
        flash('삭제 권한 없음')
        return redirect(url_for('question.datail', question_id=question_id))

    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))

#질문 추천 라우팅 함수
@bp.route('/vote/<int:question_id>')
@login_required
def vote(question_id):
    _question = Question.query.get_or_404(question_id)
    #본인글 추천X
    if g.user == _question.user:
        flash('본인 작성 글 추천 불가')
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))
