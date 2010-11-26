@echo off
ECHO ----------------------------------------
echo Creating Confluence Build Folder
rmdir /S /Q skin.influence
md skin.influence
md skin.influence\media

Echo .svn>exclude.txt
Echo Thumbs.db>>exclude.txt
Echo Desktop.ini>>exclude.txt
Echo dsstdfx.bin>>exclude.txt
Echo Build>>exclude.txt
Echo media>>exclude.txt
Echo exclude.txt>>exclude.txt

ECHO ----------------------------------------
ECHO Creating XBT File...
START /B /WAIT TexturePacker -input ..\skin\media -output .\skin.influence\media\Textures.xbt

ECHO ----------------------------------------
ECHO XBT Texture Files Created...
ECHO Building Skin Directory...
xcopy "..\skin" "skin.influence" /E /Q /I /Y /EXCLUDE:exclude.txt

del exclude.txt
