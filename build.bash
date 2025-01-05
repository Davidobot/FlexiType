rm -rf build dist
pyinstaller main.py --onefile --noconsole --name FlexiType --clean
mv dist/FlexiType.app ./FlexiType.app
rm -rf build dist