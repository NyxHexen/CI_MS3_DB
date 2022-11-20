from devbus import app, os


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True) # REMOVE BEFORE DEPLOYMENT AND SUBMISSION