from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
import tensorflow as tf
import hashlib
import random
import codecs
import certifi
import jwt
import h5py


# DB
client = MongoClient('mongodb+srv://test:sparta@cluster0.zxyme.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.recycleKing

# jwt Secret key
SECRET_KEY = 'recycleKing'

# flask app
app = Flask(__name__)

# model
model = load_model('static/model/model.h5')




############ url ################
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"id": payload['id']})
        return render_template('recycle.html', id=user_info['id'])

    except jwt.ExpiredSignatureError: #
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))

    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/webcam')
def webcam():
    return render_template('Webcam.html')


@app.route('/login')
def login():
    return render_template('index.html')

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/recycle')
def recycle():
    return render_template('recycle.html')

@app.route('/result')
def result():
    return render_template('result.html')


############ api ################

# 로그인
@app.route('/api/login', methods=['POST'])
def api_login():
    id = request.form['id']
    pw = request.form['pw']

    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    doc = {
      'id': id,
      'pw': pw_hash
    }

    result = db.users.find_one(doc)
    print(result)

    # 발견시 JWT 토큰 만들고 발급
    if result is not None:
        payload = {
           'id': id,

        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})

    else:
        return jsonify({'result': 'fail', 'msg': '동호수/비밀번호가 일치하지 않습니다.'})


# 회원가입
@app.route('/api/sign_up', methods=['POST'])
def api_sign_up():

    id = request.form['id']
    pw = request.form['pw']
    score = 0

    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    if db.users.find_one({'id':id}): # 중복확인
        return jsonify({'result': 'fail', 'msg': '다른 사람 집입니다.'})

    doc = {
        'id': id,
        'pw': pw_hash,
        'score' : score
    }

    db.users.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '회원가입 성공'})


# 동&호수 중복 확인
@app.route('/api/check_id', methods=['POST'])
def api_check_id():
    id = request.form['id']

    if db.users.find_one({'id': id}):
        return jsonify({'result': 'fail', 'msg': '다른 사람 집입니다.'})
    else:
        return jsonify({'result': 'success', 'msg': '본인 집입니다.'})


# recycle check
@app.route('/api/recycle_check', methods=['POST'])
def api_recycle_check():
    waste_name = request.form['waste'] # 쓰레기통이름
    waste_img = request.files['waste_img']  # 이미지 파일


    # 이미지 파일 저장
    extension = waste_img.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'{mytime}'
    save_to = f'static/img/trash/{filename}.{extension}'
    waste_img.save(save_to)

    # 이미지로 정답 예측
    test_datagen = ImageDataGenerator(rescale=1. / 255)
    test_dir = 'static/img'
    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=(224, 224),
        color_mode="rgb",
        shuffle=False,
        class_mode=None,
        batch_size=1)
    pred = model.predict(test_generator)

    # 예측값
    for i in pred:
        pred_name = np.argmax(i)
        print('what pred name?', pred_name)

        if pred_name == 0:
            pred_name = 'metalFile'
        elif pred_name == 1:
            pred_name = 'paperFile'
        elif pred_name == 2:
            pred_name = 'glassFile'
        elif pred_name == 3:
            pred_name = 'paperFile'
        elif pred_name == 4:
            pred_name = 'plasticFile'
        elif pred_name == 5:
            pred_name = 'trashFile'


    # 정답 확인
    if pred_name == waste_name:
        result = 'true'
    else:
        result = 'false'

    return jsonify({'result':result})

# recycle score submit
@app.route('/api/submit', methods=['POST'])
def api_submit():
    login_user = isLogin()
    score_recieve = int(request.form['score'])
    update_score = login_user['score'] + score_recieve
    db.users.update_one(login_user, {'$set': {'score': update_score}})

    return jsonify({'result': 'true'})

# result
@app.route("/api/result", methods=["GET"])
def submit_get():
    ranking_list = list(db.users.find({}, {'_id': False}))
    return jsonify({'ranking':ranking_list})




########## func #############
def isLogin():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"id": payload['id']})
        return user_info
    except:
        return False


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
