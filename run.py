from application import app
import sys


app.run(debug=True,host='0.0.0.0',port=int(sys.argv[1]),threaded=True)

