# backend/app.py
from backend import create_app  # Ensure this import is correct

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
