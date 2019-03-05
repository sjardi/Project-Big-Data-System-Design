from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/search/<keyword>')
def search(keyword):
    return '{"results": [{"title": "Test article 1", "url": "https://google.com", "description":"Welcome to this test article. In this test article I will talk about..."}]}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')