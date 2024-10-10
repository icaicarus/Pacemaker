#!/usr/bin/env python3.8
from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)  # debug mode for development
