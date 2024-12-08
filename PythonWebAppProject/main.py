#Now here we are going to import the website package, use that create_app() function inside __init__.py file and run it and create an app

from website import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)