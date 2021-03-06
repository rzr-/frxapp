# Basic Flask web app with CRUD
### Deployment to Heroku
1. Create new app on Heroku
2. Attach Posgres DB to the app
3. Set Enviromental Variables

| ENVVAR  | VALUE |
| ------------- | ------------- |
| SECRET_KEY | random_secret_key |
| LONG_BIG_PASSWORD_SALT_VERY_SALTED | random_secret_salt |
| SOME_SECRET_KEY | some_more_secret_key |
| SQLALCHEMY_DB_URI | Check Postgres credentials: ```postgres://[username]:[password]@[server]:[port]/[db]```  |
| MAIL_SERVER | i.e. smtp.gmail.com |
| MAIL_PORT | i.e. 465 for gMail |
| MAIL_USERNAME | email address |
| MAIL_PASSWORD | pa$$word |
| MAIL_DEFAULT_SENDER | email address|

4. Connect git repository to the app and deploy
5. run ```bash``` console:
    - ```$ flask shell```
    - import DB and models
    ```from app.models import User```
    ```from app import db```
    - Create DB tables
    ```db.create_all()```
    - Create admin user
    ```admin = User(email="admin@email.x", username="admin", password="passowrd", type="2")```
    - Add admin user
    ```db.session.add(admin)```
    - Commit changes to the db
    ```db.session.commit()```
                