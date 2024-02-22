import functools
from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Question, Answer
from ..forms import AnswerForm

bp = Blueprint('answer', __name__, url_prefix='/answer')

#로그인 필수 처리 데코레이터 : @login_required
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        #login여부 check
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            print(f'_next:{_next}')
            return redirect(url_for('auth.login', next=_next))

        return view(*args, **kwargs)

    return wrapped_view #java:무명/익명 class


@bp.route('/create/<int:question_id>', methods=('POST',))
@login_required
def create(question_id):
    print('-'*50)
    print(f'question_id:{question_id}')
    print('-' * 50)

    form = AnswerForm()

    question = Question.query.get_or_404(question_id)

    #content
    #request : request객체는 플라스크 내장 겍체, 브라우저 요청을 처리

    if form.validate_on_submit():

        contents = request.form['contents']
        print(f'contents:{contents}')

        #답변등록
        answer = Answer(question=question, contents=contents, create_date=datetime.now(), user=g.user)
        db.session.add(answer) #저장
        db.session.commit() #commit

        return redirect(url_for('question.detail', question_id=question_id))

    return render_template('question/question_detail.html', question=question, form=form)

#수정 : modify
@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)

    #권한 체크
    if g.user != answer.user:
        flash('수정 권한 없음')
        return redirect( url_for('question.detail', question_id=answer.question.id))

    if request.method == 'POST': #POST 처리
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer) #수정 함수/form데이터를 수정
            answer.modify_date = datetime.now() #수정일

            db.session.commit()

            return redirect( url_for('question.detail', question_id=answer.question.id)) #질문 상세로 이동

    else: #GET 방식
        form = AnswerForm(obj=answer)

    return render_template('answer/answer_form.html', form=form)

#삭제 : delete
@bp.route('/delete/<int:answer_id>') #GET만 있음
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id

    # 권한 체크
    if g.user != answer.user:
        flash('삭제 권한 없음')
    else:
        db.session.delete(answer)
        db.session.commit()

    return redirect( url_for('question.detail', question_id=question_id))

#답변 추천
@bp.route('/vote/<int:answer_id>')
@login_required
def vote(answer_id):
    _answer = Answer.query.get_or_404(answer_id)
    if g.user == _answer.user:
        flash('본인 댓글 추천 불가')
    else:
        _answer.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=_answer.question.id))
