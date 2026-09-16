import os
from ollmw import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("WEB_PORT"), debug=True)
