from flask import Flask
import threading
import subprocess
from waitress import serve

app = Flask(__name__)

@app.route("/")
def home():
  return "noticeMeSempai"

def run():
  if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)

def thread_run():
  t = threading.Thread(target=run)
  t.start()
  try:
    subprocess.run(["py","Neomi.py"])
  except:
    subprocess.run(["python3","Neomi.py"])

thread_run()

