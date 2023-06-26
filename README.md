Brownian Motion Simulator v.1.1
Levy App Simulator v.1.1

## bug-fix
- Fixed Bug with Errors during fast changing value of Speed 
- Added margins in view of Levy Flight 
- Multiplied available value of Moles in slider

## how to basic:
0. Package needed to run these apps
    ``` PyQtCore ```
    ``` NumPy ```
1. window manipulation:
    ```pyqt5-tools.exe designer```
2. do smth then save file in designer to .ui file
    DO NOT CONVERT IN THIS GUI BCZ ITS BROKEN
3. instead convert the .ui use the command
    ```pyuic5.exe .\window.ui -o window_ui.py```
4. file window_ui.py is QT converted to python code
5. DO NOT EDIT OUTPUT FILE BCZ IT MAY BE DELETED WHEN RECOMPILING .ui file
6. you may edit window_ui.py file to change application behavior
7. my honda eats through oil like Kononowicz
8. enjoy!
9. For increase code readability i used black:
    ```pip install git+https://github.com/psf/black```
    ```black <filename>```
10. And the most important!!! Run both app with Python 3.11.3 commands
   ``` python .\LevyApp.py ```
   ``` python .\Brownian.py ```