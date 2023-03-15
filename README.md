# Rok_title_bot
Automate title giver for rise of kingdom by detect shared location in chat room

![Capture](https://user-images.githubusercontent.com/46108793/221357768-639f6061-c1d5-4d71-9b61-f520d085911d.jpg)


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
* Android Debug Bridge (adb)
    https://developer.android.com/studio/releases/platform-tools
* Tesseract-OCR 5.3.0
    https://github.com/UB-Mannheim/tesseract/wiki
* BlueStack version 5
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
3) Install adb in **.\Rok-BotgiverTitle\platform-tools_r34.0.0-windows**
4) Install Tesseract-OCR in **.\Rok-BotgiverTitle\Tesseract-OCR**
5) Edit config.ini 
6) Open rise of kingdom on bluestack and open chat room for giving the title
7) Start the bot 
    ```python
    python3 main.py
    ```
8) Enjoy!
