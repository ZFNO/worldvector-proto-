@echo off
python update_beta.py

git add .

git commit -m %*

git push