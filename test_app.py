import streamlit
from streamlit.testing.v1 import AppTest

def test_app_starts():
    at = AppTest.from_file("app.py")
    at.run()
    assert not at.exception
    print("App loaded successfully without exceptions.")

if __name__ == "__main__":
    test_app_starts()
