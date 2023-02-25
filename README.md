# Rok_title_bot
Automate title giver for rise of kingdom by detect shared location in chat room

### Feature
* Automatic give title to player
  - [X] Duke
  - [ ] Architect
  - [ ] Science
  - [ ] Justice
* Automatic search player location
* Support kvk map that has forge
* Auto detect network unstable

### Requirement
* Python ver 3+
* Adb
* Tesseract-OCR
* BlueStack version
   - Turn on Android debug bridge (adb)
   - Using resolution 1600x900

### Limitation (1.0)
* Support only **duke** in chat room
* Cannot notify to user
* Cannot detect **"Done"** keyword
* Not support reCaptcha

### Installation
1) Clone this project
    ```bash
    git clone https://github.com/Rctz/Rok_title_bot.git
    ```
2) install required python packages
    ```bash
    pip install -r requirement.txt
    ```
3) Set your tesseract-ocr path in config.py
4) Open rise of kingdom on bluestack and open chat room for give title
5) Run bot 
    ```python
    python3 main.py
    ```
6) Enjoy!
