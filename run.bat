@echo off
call ..\venv\Scripts\activate
pip install -r requirements.txt
nb start --reload
pause