from models import User, Link, db
from app import app

"""drop all existing tables"""
db.drop_all()
db.create_all()

#Add users
testa = User.signup(
    first_name = 'testa',
    last_name = 'testa',
    email = 'testa@links.com',
    password='helloworld'
)

testb = User.signup(
    first_name = 'testb',
    last_name = 'testb',
    email = 'testb@links.com',
    password='helloworld'
)

testc = User.signup(
    first_name = 'testc',
    last_name = 'testc',
    email = 'testc@links.com',
    password='helloworld'
)


db.session.add_all([testa, testb, testc])
db.session.commit()

#add links
user_id =  User.query.filter_by(first_name = "testa").first().id

linka = Link(
            platform = 'twitter',
            link= 'www.twitter.com',
            user_id = user_id
        )

linkb = Link(
            platform = 'facebook',
            link= 'www.facebook.com',
            user_id = user_id
        )

linkc = Link(
            platform = 'instagram',
            link= 'www.instagram.com',
            user_id = user_id
        )

db.session.add_all([linka, linkb, linkc])
db.session.commit()
