from application import app
import sys


app.run(debug=True,port=int(sys.argv[1]),threaded=True)

