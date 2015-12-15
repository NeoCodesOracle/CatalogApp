from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catalog_database import Base, User, Category, Item

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy users
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             img_url='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

User2 = User(name="Ethan Melgar", email="melgarin@udacity.com",
             img_url='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User2)
session.commit()

# --------------------------------------------- Create first category
category1 = Category(
       user_id=1,
       name="Soccer",
       img_url="http://www.beachfieldhouse.com/imgs/"
              "CASLs15CoachesMeeting.jpg")
session.add(category1)
session.commit()

# Create some items and add them to our first category
item1 = Item(
       user_id=1,
       name="Soccer Ball",
       description="Kick your game up a notch with the Nike Mercurial Veer"
              "soccer ball! The 26-panel construction provides strength and"
              "symmetry to this colorful ball. Its bold design makes it easy"
              "to see when it's flying into the goal.",
       price="$25.00",
       img_url="http://www.sportsauthority.com/graphics/product_images/"
              "pTSA-19856023nm.jpg",
       category=category1)
session.add(item1)
session.commit()

item2 = Item(
       user_id=1,
       name="Adidas Kids' Messi 15.3 IN J Low Soccer Shoes",
       description="Your rising star will play like the pros in these adidas"
              "kids' Messi 15.3 IN J low soccer shoes. They're made with a"
              "3D synthetic leather upper and an indoor-optimized outsole for"
              "total comfort and control even when the pressure's on.",
       price="$55.00",
       img_url="http://www.sportsauthority.com/graphics/product_images/"
              "pTSA-19856023nm.jpg",
       category=category1)
session.add(item2)
session.commit()

item3 = Item(
       user_id=1,
       name="Nike Adult Neymar Mercurial Lite Soccer Shin Guards",
       description="Play fearlessly without worrying about getting hurt in"
              "these Nike adult Neymar Mercurial Lite soccer shin guards."
              "Developed with the input of the star player himself, these"
              "guards feature a contoured left- and right-specific design"
              "for the perfect anatomical fit. The dense foam backing and"
              "low-profile shell dampen painful impact for max protection.",
       price="$55.00",
       img_url="http://www.sportsauthority.com/graphics/product_images/"
              "pTSA-21028790p275w.jpg",
       category=category1)
session.add(item3)
session.commit()

item4 = Item(
       user_id=1,
       name="Nike Adult Classic Goalkeeper Gloves",
       description="These Nike adult Classic goalkeeper gloves supply"
              "everything you need to keep the ball from slipping through."
              "They're designed with a traditional cut for complete comfort"
              "and smooth latex foam for excellent grip. A Tri-Vario"
              "wraparound wristband supplies a customized fit and allows for"
              "easy adjustments on the pitch.",
       price="$55.00",
       img_url="http://www.sportsauthority.com/graphics/product_images/"
              "pTSA-21028790p275w.jpg",
       category=category1)
session.add(item4)
session.commit()

item5 = Item(
       user_id=1,
       name="Adidas Women's Tiro 15 Training Soccer Pants",
       description="These Nike adult Classic goalkeeper gloves supply"
              "everything you need to keep the ball from slipping through."
              "They're designed with a traditional cut for complete comfort"
              "and smooth latex foam for excellent grip. A Tri-Vario"
              "wraparound wristband supplies a customized fit and allows for"
              "easy adjustments on the pitch.",
       price="$35.00",
       img_url="http://www.sportsauthority.com/graphics/product_images/"
              "pTSA-19935689p275w.jpg",
       category=category1)
session.add(item5)
session.commit()

# --------------------------------------------- Create second category
category2 = Category(
       user_id=2,
       name="Curling",
       img_url="http://www.missoulacurlingclub.com/wp-content/uploads/2014/"
              "03/Curling_stones_on_rink_with_visible_pebble.jpg")
session.add(category2)
session.commit()

# Create some items and add them to our second category
item1 = Item(
       user_id=2,
       name="Curling Stone",
       description="The curling stone (also sometimes called a rock in North"
              "America) is made of granite and is specified by the World"
              "Curling Federation, which requires a weight between 38 and 44"
              "pounds (17 and 20 kg) a maximum circumference of 36 inches"
              "(910 mm) and a minimum height of 4.5 inches (110 mm).",
       price="$105.00",
       img_url="http://www.sportsauthority.com/graphics/product_images/"
              "pTSA-19856023nm.jpg",
       category=category2)
session.add(item1)
session.commit()

# --------------------------------------------- Create third category

# Create third category
category3 = Category(
       user_id=2,
       name="Cricket",
       img_url="http://www.cricketcontrol.info/wp-content/uploads/2013/11/"
              "383739-ian-bell-england-cricket-620x349.jpg")
session.add(category2)
session.commit()

# Create fourth category
category4 = Category(
       user_id=1,
       name="Cross Country",
       img_url="http://www.issaquahpress.com/wp-content/uploads/2015/04/"
              "TrackSiriLHS-20150423.jpg")
session.add(category4)
session.commit()

# Create fifth category
category5 = Category(
       user_id=1,
       name="Archery",
       img_url="https://i.ytimg.com/vi/-HR_i7lLSRA/maxresdefault.jpg")
session.add(category5)
session.commit()
