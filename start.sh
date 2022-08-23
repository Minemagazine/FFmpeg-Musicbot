clear
youtube-dl --rm-cache-dir
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
python3 index.py
