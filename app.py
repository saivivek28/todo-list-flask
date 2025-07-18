from flask import Flask , render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
app = Flask(__name__)

client =MongoClient("mongodb+srv://saivivek_28:ccH22bIlkMEE7Yui@cluster0.mfgk2ns.mongodb.net/")
database = client["todo"]
collection = database["task"]
@app.route('/home')
def table():
    details = collection.find()
    tasks = list(details)
    return render_template("home.html", tasks = tasks)

@app.route('/register', methods = ['POST'])
def register():
    title = request.form["title"]
    description = request.form["description"]
    collection.insert_one({"title":title, "description": description})
    return redirect("/home")

@app.route('/create')
def create():
    return render_template("create.html")

@app.route('/update/<_id>', methods = ['GET', 'POST'])
def update(_id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        collection.update_one({"_id":ObjectId(_id)}, {"$set": {"title": title, "description":description}})
        return redirect('/home')
    elif request.method == "GET":
        task = collection.find_one({"_id":ObjectId(_id)})
        return render_template('update.html', task = task)
    
    
@app.route("/delete/<_id>")
def delete(_id):
    task = collection.delete_one({"_id":ObjectId(_id)})
    return redirect('/home')
if __name__ == "__main__":
    app.run(debug=True)