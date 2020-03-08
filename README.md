# SageDorms
CS133 room draw

Milestone 2: https://www.overleaf.com/1142286357jtkcpvvqnxyw

SHARED FOLDER:
https://drive.google.com/drive/folders/1OzhyUGDP3FL8qc6LNfxDPc3itNJeBiOh?usp=sharing

Google Doc:
https://docs.google.com/document/d/1i_KFfRNegjPZRX6PrNN8XlIa9H4p8LpQQXTtKo-DGWg/edit?fbclid=IwAR3b6Ey94koVqntcKDE-PvlmGKSEq5ysap1M47hqCpkEblObW2VAjWd5_28

Milestone 0:
https://docs.google.com/document/d/1oqUyrVeIod7JRTgFklCOZwkpGrdnPXMqxyjEtXB8oyk/edit

## How to install stuff to run the sagedorm_db app:

### Python + Jinja
1. Check if you have Python 3 by typing `python3`. If a python command line pops
   up, skip to step 3
2. Run `brew install python`. Go to step 1.
3. Run `echo "alias python=python3" >> ~/.bashrc` and 
`echo "alias python=python3" >> ~/.zshrc`
4. Run `pip3 install jinja2`. Jinja is for printing things from Python and Flask

### MySQL

1. Install mySQL from [this website](https://dev.mysql.com/downloads/mysql/)
2. Also install the mySQL workbench from
[here](https://dev.mysql.com/downloads/file/?id=492445)
3. I think yall have a Mac so to start the mySQL server:
    - go to System Preferences > MySQL (bottom row) > Initialize Database > type
      `databases133` into the password field and select the Legacy Password
      Encryption option (you can make this password whatever you want, but in
      the sagedorm_db app the password is hardcoded as databases133)
    - click Initialize Database

### Python Connector

1. Run `pip3 install mysql-connector` on the terminal

## How to run the demo app:

1. At the root of this directory, run `python sagedorm_db.py`. This intializes
   the SageDorms database.
2. Open the mySQL Workbench app. It's somewhere in your apps folder. Then click
   the rectangle that says "Local instance 3306" underneath MySQL connections.
   Type in the password if prompted (databases133 if you didn't change it).
3. In the menu bar, click File > Open SQL Script (or press Shift + Command + O)
   and select the Pop_Students.sql file in the test_files folder.
4. Double click sagedormdb in the sidebar. Then run the sql file by clicking the
   thunderbolt above the console. This just adds students to register housing
   for.
5. Now open a new terminal window and run `python app.py`. It should say
   something like "Running on http://127.0.0.1:5000/"
6. Open your web browser and type "localhost:5000" in the URL. In the Student ID
   field, type in an existing sid from the database. Click submit and now the
   housing is registered!
