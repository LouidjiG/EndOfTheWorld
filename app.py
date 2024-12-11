from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/wallpapers/<path:filename>')
def wallpapers(filename):
    return send_from_directory('/user/gravelel/Téléchargements/EndOfTheWorld/Wallpapers', filename)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
