from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbjungle

@app.route('/')
def home():
   return render_template('index.html')


@app.route('/api/list', methods=['GET'])
def show_star():
   result = list(db.mystar.find({},{'_id':0}).sort('like', -1))
   return jsonify({'result':'success', 'star_list':result})


@app.route('/api/like', methods=['POST'])
def like_star():
    name_receive = request.form['name_give']
    star = db.mystar.find_one({'name': name_receive}, {'_id': 0})
    new_like = star['like'] + 1
    db.mystar.update_one({'name': name_receive}, {'$set': {'like': new_like}})
    return jsonify({'result':'success'})


@app.route('/api/delete', methods=['POST'])
def delete_star():
    name_receive = request.form['name_give']
    db.mystar.delete_one({'name': name_receive})
    return jsonify({'result':'success'})


if __name__ == '__main__':
   app.run(host='0.0.0.0')
