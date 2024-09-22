from flask import Flask, render_template
import textile


#############################################

# open and read re-formatted html text

with open('final.txt', 'r') as f:
  data2 = f.read()
  data1 = textile.textile(data2)
  f.close()
  print("final.txt read....\n\n")


########    run Flask server   ########

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    #global data1
    return render_template("basic2.html",test2=data2)

app.run()