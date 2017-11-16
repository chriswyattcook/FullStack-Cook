from pymongo import MongoClient
import hashlib
import glob

# Create a link to our mongo database
client = MongoClient()

x = raw_input("This will erase your db! Continue? (y,N):")
if x.lower() == 'y':
    client['memes_db']['images'].delete_many({})
    client['memes_db']['users'].delete_many({})
    client['memes_db']['memes'].delete_many({})

    people = [
        {
            '_id' : 1,
            'first':'Joe',
            'last':'Black',
            'email':'joe.black@yahoo.com',
            'username':'jblack',
            'password':hashlib.sha224('password1234').hexdigest()
        },
        {
            '_id' : 2,
            'first':'Cindy',
            'last':'Smith',
            'email':'bluewhalelover@gmail.com',
            'username':'bluewhalesrock',
            'password':hashlib.sha224('blueblueblue').hexdigest()
        },
        {
            '_id' : 3,
            'first':'Fred',
            'last':'Flintsone',
            'email':'fredthestud@gmail.com',
            'username':'fred',
            'password':hashlib.sha224('passfredpass').hexdigest()
        },
        {
            '_id' : 4,
            'first':'George',
            'last':'Bush',
            'email':'gwbush@gmail.com',
            'username':'theprez',
            'password':hashlib.sha224('iamtheprez').hexdigest()
        }
    ]


    for p in people:
        idx = client['memes_db']['users'].insert(p)


    images = [
        {
            '_id' : 1,
            'file_name':'archer.jpg',
            'tags':['archer','funny','cartoon'],
            'abs_path':'/var/www/html/memes_blank/',
            'rel_path':'memes_blank/',
            'owner_id': -1
        },
        {
            '_id' : 2,
            'file_name':'does_not_simply.jpg',
            'tags':['Sean','Bean','ned','stark','simply'],
            'abs_path':'/var/www/html/memes_blank/',
            'rel_path':'memes_blank/',
            'owner_id': -1
        },
        {
            '_id' : 3,
            'file_name':'firestarter.jpg',
            'tags':['fire','starter','creepy'],
            'abs_path':'/var/www/html/memes_blank/',
            'rel_path':'memes_blank/',
            'owner_id': -1
        },
        {
            '_id' : 4,
            'file_name':'leanardo_is_awesome.jpg',
            'tags':['leanardo','decaprio'],
            'abs_path':'/var/www/html/memes_blank/',
            'rel_path':'memes_blank/',
            'owner_id': -1
        },
        {
            '_id' : 5,
            'file_name':'mesmerized.jpg',
            'tags':['mesmerized','girl','eyes'],
            'abs_path':'/var/www/html/memes_blank/',
            'rel_path':'memes_blank/',
            'owner_id': -1
        },
        {
            '_id' : 6,
            'file_name':'not_gay.jpg',
            'tags':[],
            'abs_path':'/var/www/html/memes_blank/',
            'rel_path':'memes_blank/',
            'owner_id': -1
        },
        {
            '_id' : 7,
            'file_name':'thinkaboutit.jpg',
            'tags':[],
            'abs_path':'/var/www/html/memes_blank/',
            'rel_path':'memes_blank/',
            'owner_id': -1
        }
    ]


    for img in images:
        idx = client['memes_db']['images'].insert(img)


    memes = [
        {
            '_id' : 1,
            'file_id': 1,
            'owner_id': 1,
            'top_text': 'This is the top text',
            'bot_text':'And we have bottom text',
            'style_info': {'text-color':(0,0,0),'text-size':24}
        },
        {
            '_id' : 2,
            'file_id': 1,
            'owner_id': 1,
            'top_text': 'This archer again',
            'bot_text':'Your Stupid',
            'style_info': {'text-color':(0,0,0),'text-size':24}
        },
        {
            '_id' : 3,
            'file_id': 5,
            'owner_id': 2,
            'top_text': 'You smell good',
            'bot_text':'when your sleeping...',
            'style_info': {'text-color':(0,0,0),'text-size':24}
        }
    ]


    for meme in memes:
        idx = client['memes_db']['memes'].insert(meme)