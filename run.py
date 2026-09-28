"""
run.py
Entry point for running the Flask Hospital Management System.
Configured for local execution and production container runners.
"""

import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    # Run the application (Debug off by default per security requirements)
    app.run(host=host, port=port, debug=False)
