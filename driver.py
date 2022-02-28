from main import *
from cpu import *

app = App()

while True:
    print(app.state)
    if app.state == "win" or app.state == "loss":
        app.reset()