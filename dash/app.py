from layout import app, applayout
from dash import Dash

if __name__ == '__main__':
    app.layout = applayout
    app.run(debug=True)
