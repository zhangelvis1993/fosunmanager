from dataweb import app
from flask import render_template

@app.errorhandler(404)
def page_not_found(e):
    return render_template('main/404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
