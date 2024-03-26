from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb+srv://Bagas99:Kataksalto98@cluster0.m9sxgje.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']
    
    max_num = db.bucket.find_one(sort=[("num", -1)])
    if max_num:
        max_num= max_num['num']
    else:
        max_num = 0
    num = max_num + 1
    doc={
        'num': num,
        'bucket': bucket_receive,
        # 0 artinya tugas belum selesai
        # 1 artinya tugas sudah selesai
        'done': 0
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': 'Data Saved!'})

# done
@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    # membuat tombol done nya aktif
    num_receive = request.form['num_give']
    db.bucket.update_one(
        # mengapa menggunakn int? karena mencegah kalo user masukan tipe data "string".
        {'num': int(num_receive)},
        {'$set': {'done': 1}}
    )
    return jsonify({'msg': 'Update Done!'})

# delete
@app.route("/bucket/delete", methods=["POST"])
def bucket_delete():
    num_receive = request.form['num_give']
    db.bucket.delete_one(
        {'num': int(num_receive)}
    )
    return jsonify({'msg': 'Data Deleted!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'buckets': buckets_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)