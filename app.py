

# import webbrowser
# import time
# from flask import Flask, render_template

# app = Flask(__name__)

# urls = [
#    "http://127.0.0.1:5550/register_table",
#    "http://127.0.0.1:5550/get_secret_shameer",
#     "http://127.0.0.1:5551/register_table",
#    "http://127.0.0.1:5551/get_secret_shameer",
# #    "http://127.0.0.1:5552/register_table",
# #    "http://127.0.0.1:5552/get_secret_shameer",
# #     "http://127.0.0.1:5553/register_table",
# #     "http://127.0.0.1:5553/get_secret_shameer",
# #     "http://127.0.0.1:5554/register_table",
# #     "http://127.0.0.1:5554/get_secret_shameer",
  
  
#    "http://127.0.0.1:5540/vehicle" ,
#    "http://127.0.0.1:5540/connect",
# ]

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/openurls')
# def open_urls():
#     for url in urls:
#         webbrowser.open(url,new=1)
      
#         time.sleep(5)  # Adjust the time gap as needed (in seconds)
#     return "URLs opened successfully!"

# if __name__ == '__main__':
#     app.run(debug=True)
# ///////////////////////////////////////////////////////////////////////////////

# import time
# import webbrowser
# from selenium import webdriver
# from flask import Flask, render_template

# app = Flask(__name__)

# urls = [
#     "http://127.0.0.1:5550/register_table",
#     "http://127.0.0.1:5550/get_secret_shameer",
#     "http://127.0.0.1:5551/register_table",
#     "http://127.0.0.1:5551/get_secret_shameer",
#     # Add more URLs as needed
#     "http://127.0.0.1:5540/vehicle",
#     # "http://127.0.0.1:5540/connect",
# ]

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/openurls')
# def open_urls():
#     options = webdriver.ChromeOptions()
#     options.add_argument('headless')  # This will open the browser in a hidden manner
#     driver = webdriver.Chrome(options=options)
    
#     for url in urls:
#         driver.get(url)
#         time.sleep(5) 
        
#     driver.quit()
#     webbrowser.open("http://127.0.0.1:5540/connect")
     
#     return "URLs opened successfully!"

# if __name__ == '__main__':
#     app.run(debug=True)
# //////////////////////////////////////////////////////////////////////////////////////////////////


import time
import webbrowser
from selenium import webdriver
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

urls = [
    "http://127.0.0.1:5550/register_table",
    "http://127.0.0.1:5550/get_secret_shameer",
    "http://127.0.0.1:5551/register_table",
    "http://127.0.0.1:5551/get_secret_shameer",
    # Add more URLs as needed
    "http://127.0.0.1:5540/vehicle",
    # "http://127.0.0.1:5540/connect",
]

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('open_urls')
def open_urls():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # This will open the browser in a hidden manner
    driver = webdriver.Chrome(options=options)
    
    for url in urls:
        socketio.emit('message', f"Connecting to {url}")
        driver.get(url)
        time.sleep(5) 
        socketio.emit('message', f"Successfully connected to {url}")
        
    driver.quit()
    webbrowser.open("http://127.0.0.1:5540/connect")
     
    return "URLs opened successfully!"

if __name__ == '__main__':
    socketio.run(app, debug=True)
