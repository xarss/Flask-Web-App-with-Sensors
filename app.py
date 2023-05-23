from flask import Flask, render_template, session, g
from controllers.app_controller import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)