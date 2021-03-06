from flask import Flask,render_template,request,redirect,url_for
from deepzoom import *
import os
import shutil
#import asyncio
import threading
from drive import *

app = Flask(__name__)

@app.route('/')  
def upload():  
    try:
        folder = './uploads'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e)) 
    except:
        pass
    return render_template("file_upload_form.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        file_id = request.form['file'].strip()
        destination = './uploads/alpha'
        download(file_id.split('/')[5] , destination)
        if os.path.exists("./static/alpha.dzi"):
            os.remove("./static/alpha.dzi")
        if os.path.exists("./static/alpha_files"):
            shutil.rmtree("./static/alpha_files") 
        t = threading.Thread(target=convert, args=(destination,))
        t.start()
        return redirect(url_for("home"))

@app.route('/home')
def home():
    return render_template('home.html')


if __name__ == '__main__' :
        app.run(debug=True)
