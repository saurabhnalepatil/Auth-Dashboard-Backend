from app import app


@app.route("/api/sau", methods=["GET"])
def sau_login():
    try:
        return "Login successful"
    except Exception as e:
        return "Error: {}".format(e)
