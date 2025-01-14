rm -rf build dist
pyinstaller main.py --onefile --noconsole --name FlexiType --clean --icon icons/flexitype-icon.png --add-data="icons/flexitype-icon.png:icons"
mv dist/FlexiType.app
rm -rf build