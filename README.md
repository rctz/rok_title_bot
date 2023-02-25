# Rok_title_bot
Automate title giver for rise of kingdom by detect shared location in chat room

![Capture (1)](https://user-images.githubusercontent.com/46108793/221348786-a9fa15c5-4e7d-432a-a5df-57868ad748df.jpg)


### Feature
* Automatic give title to player
  - [X] Duke
  - [ ] Architect
  - [ ] Science
  - [ ] Justice
* Automatic search player location
* Support kvk map that has fog
* Auto detect network unstable

### Requirement
* Python 3.8+
* Adb
* Tesseract-OCR 5.3.0
    https://github.com/UB-Mannheim/tesseract/wiki
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
3) Install Tesseract-OCR in **.\Rok-BotgiverTitle\Tesseract-OCR**
4) Open rise of kingdom on bluestack and open chat room for give title
5) Start the bot 
    ```python
    python3 main.py
    ```
6) Enjoy!
