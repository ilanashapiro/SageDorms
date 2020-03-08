# SageDorms
CS133 room draw

Milestone 2: https://www.overleaf.com/1142286357jtkcpvvqnxyw

SHARED FOLDER:
https://drive.google.com/drive/folders/1OzhyUGDP3FL8qc6LNfxDPc3itNJeBiOh?usp=sharing

Google Doc:
https://docs.google.com/document/d/1i_KFfRNegjPZRX6PrNN8XlIa9H4p8LpQQXTtKo-DGWg/edit?fbclid=IwAR3b6Ey94koVqntcKDE-PvlmGKSEq5ysap1M47hqCpkEblObW2VAjWd5_28

Milestone 0:
https://docs.google.com/document/d/1oqUyrVeIod7JRTgFklCOZwkpGrdnPXMqxyjEtXB8oyk/edit

## How to install stuff to run the hello-world app:

### Python 3
1. Check if you have Python 3 by typing `python3`. If a python command line pops
   up, skip to step 3
2. Run `brew install python`. Go to step 1.
3. Run `echo "alias python=python3" >> ~/.bashrc`

### MySQL

1. Install mySQL from [this website](https://dev.mysql.com/downloads/mysql/)
2. Also install the mySQL workbench from
[here](https://dev.mysql.com/downloads/file/?id=492445)
3. I think yall have a Mac so to start the mySQL server:
    - go to System Preferences > MySQL (bottom row) > Initialize Database > type
      `databases133` into the password field and select the Legacy Password
      Encryption option (you can make this password whatever you want, but in
      the hello-world app the password is hardcoded as databases133)
    - click Initialize Database

### Python Connector

1. Run `pip3 install mysql-connector` on the terminal

Now you can run the `hello-world.py` app! If you make changes or notice a bug
say so on the messenger group chat or put it in this README.md file.
