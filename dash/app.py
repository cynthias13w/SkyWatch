from layout import applayout
from dash import Dash

app = Dash()

if __name__ == '__main__':
    app.layout = applayout
    app.run(debug=True)
