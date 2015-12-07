from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catalog_database import Category, Base, User, Item

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database and
# represents a "staging zone" for all the objects loaded into the database
# session object. Any change made against the objects in the session won't be
# persisted into the database until you call session.commit(). If you're not
# happy about the changes, you can revert all of them back to the last commit
# by calling session.rollback()
session = DBSession()


# Create dummy user 
User1 = User(
   name="Rob the Chicken",
   email="tinnyTim@udacity.com",
   img_url=("https://cdn4.iconfinder.com/data/icons/"
      "simplus-danger-and-warning-icons/172/Layer_16-01-128.png"))
# Add it to the database
session.add(User1)
session.commit()

# Create our first category
category1 = Category(
   user_id=1,
   name="Soccer",
   img_url="https://encrypted-tbn1.gstatic.com/images?q=tbn:"
      "ANd9GcRBc3kUspQ_RXOK4LC4wauILOUQ-ByvMPlVHTIvYNIfYJYUBnPc")
# Add it to the database
session.add(category1)
session.commit()


#Create an item
item1 = Item(
   user_id=1,
   name="Nike Pitch Premier League Soccer Ball",
   description=("This Nike Pitch Premier League soccer ball features "
                  "high-contrast geometric graphics for easy tracking on the "
                  "field. The machine-stitched TPU casing provides a "
                  "consistent feel, and a reinforced rubber bladder keeps the "
                  "ball from easily deflating"),
   price="$37.50",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "pTSA-19855673nm.jpg"),
   category=category1)
# Add item to database
session.add(item1)
session.commit()

#Create an item
item2 = Item(
   user_id=1,
   name="Nike Men's Mercurial Victory V FG Low Soccer Cleats",
   description=("Blaze a trail to triumph in the NIKE Mercurial Victory V FG "
      "men's low-cut soccer cleats. Supple synthetic leather provides pure "
      "comfort and incredible ball control, while a contoured sockliner "
      "conforms to the shape of the foot to ensure custom cushioning.Molded "
      "rubber studs dig into the dirt, delivering dynamic traction and "
      "allowing aggressive side-to-side cuts."),
   price="$80.00",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "pTSA-19190467nm.jpg"),
   category=category1)
# Add item to database
session.add(item2)
session.commit()

#Create an item
item3 = Item(
   user_id=1,
   name="Adidas adiZero F50 Messi World Cup Soccer Shin Guards",
   description=("Spurred by the roar of the crowd, the great Lionel Messi "
      "knows how to put on a whirlwind performance; follow in his footsteps "
      "(if you dare) using these adidas adiZero F50 Messi World Cup soccer "
      "shin guards! The ultra-supportive sleeve is designed with TechFit "
      "technology to provide lightweight compression for a barely-there "
      "feel. The durable shield slips into the sleeve's pocket for easy "
      "prep."),
   price="$40.00",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
   "pTSA-17928448nm.jpg"),
   category=category1)
# Add item to database
session.add(item3)
session.commit()

#Create an item
item4 = Item(
   user_id=1,
   name="Adidas Metro III Soccer Sock",
   description=("This pair of adidas Metro III soccer socks offers ultimate "
      "comfort through every kick and assist. The flat-knit construction "
      "promises a better feel, while the arch compression and cushioned "
      "footbed provide support until the ref blows his final whistle."),
   price="$7.99",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "p15731093t130.jpg"),
   category=category1)
# Add item to database
session.add(item4)
session.commit()

#Create an item
item5 = Item(
   user_id=1,
   name="Nike Men's Strike Tech Soccer Pants",
   description=("Score one for sporty style with these Nike men's Strike Tech "
      "soccer pants,built with sweat-wicking Dri-FIT technology for total "
      "comfort. The gripper waistband and tapered design offer a snug fit, "
      "while zippers at the hems promise easy on/off over cleats."),
   price="$65.00",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "pTSA-20982225nm.jpg"),
   category=category1)
# Add item to database
session.add(item5)
session.commit()

#Create an item
item6 = Item(
   user_id=1,
   name="adidas Men's Tiro 15+ Graphic Pullover Soccer Hoodie",
   description=("Add a stand-out design to your training wardrobe with the "
      "adidas men's Tiro 15+ graphic pullover soccer hoodie. Its Climalite "
      "fabric is light and breathable to conduct body heat to the fabric's "
      "surface, allowing you to stay cool and dry while you warm your muscles "
      "before the game."),
   price="$65.00",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "pTSA-19323102nm.jpg"),
   category=category1)
# Add item to database
session.add(item6)
session.commit()

#Create an item
item7 = Item(
   user_id=1,
   name="NIKE Men's GPX I Short-Sleeve Soccer T-Shirt",
   description=("Tackle tough training sessions in this NIKE men's GPX I "
      "short-sleeve soccer t-shirt. Its Dri-FIT fabric pulls sweat to the "
      "fabric's surface for faster evaporation, while a mesh back panel helps "
      "cool a high-heat area of the body. Angled sleeve panels expand your "
      "range of motion for added comfort as you run, and the sublimated "
      "graphic means you don't have to sacrifice a single bit of the top's "
      "breathability for style."),
   price="$24.97",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "pTSA-17842109nm.jpg"),
   category=category1)
# Add item to database
session.add(item7)
session.commit()

#Create an item
item8 = Item(
   user_id=1,
   name="Nike Men's Academy 2 Longer Knit Soccer Shorts",
   description=("The Nike men's Academy 2 longer knit soccer shorts are made "
      "with Dri-FIT and mesh fabrics for optimal sweat-wicking comfort. The "
      "adjustable waistband offers a secure fit for high-speed play."),
   price="$12.97",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "pTSA-18977868nm.jpg"),
   category=category1)
# Add item to database
session.add(item8)
session.commit()

#Create an item
item9 = Item(
   user_id=1,
   name="SKLZ Goal-EE",
   description=("The SKLZ Goal-EE is a foldable soccer goal that opens and "
      "closes in seconds. When folded, the goal can fit just about anywhere. "
      "The 4' x 3' frame is ideal for practice or short-sided scrimmages."),
   price="$39.99",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "p11842185nm.jpg"),
   category=category1)
# Add item to database
session.add(item9)
session.commit()

#Create an item
item10 = Item(
   user_id=1,
   name="PUMA Adult evoPOWER Super Goalkeeper Gloves", 
   description=("When it's your time to shine, these PUMA evoPOWER Super "
      "goalkeeper gloves make sure you do. Removable FLEXTEC 2 finger "
      "inserts lock to prevent hyperextension, giving you the confidence "
      "to get in front of the hardest shots. A twin wrap thumb maximizes "
      "ball contact, while Absorb Grip latex on the palm promises control "
      "in all weather conditions. A full-length latex strap and separate "
      "WrapTEC strap add key wrist support."),
   price="$120.00",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "pTSA-21579433nm.jpg"),
   category=category1)
# Add item to database
session.add(item10)
session.commit()

# Create our second category
category2 = Category(user_id=1, 
   name="Football",
   img_url="https://encrypted-tbn2.gstatic.com/images?q=tbn:"
      "ANd9GcSSgzR1blg9_wBmcxN3J3r9bjagY6IfCmBP3TZAR_Hl4A0mkXUKiA")
# Add it to the database
session.add(category2)
session.commit()

#Create an item
item1 = Item(
   user_id=1,
   name="Wilson Official NFL Game Football", 
   description=("Play like the pros with the Wilson official NFL game "
      "football. This football boasts a genuine leather cover with the "
      "official lace pattern, and the exclusive leather has a deeper "
      "pebble pattern and firmer texture. An official NFL shield verifies "
      "the authenticity."),
   price="$99.99",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "pTSA-9890798nm.jpg"),
   category=category2)
# Add item to database
session.add(item1)
session.commit()

#Create an item
item2 = Item(
   user_id=1,
   name=("Nike Men's Vapor Untouchable Low Football Cleats - "
      "Super Bowl Edition"),
   description=("Become the fastest, most fearsome guy on the field in these "
      "Nike men's Vapor Untouchable Super Bowl mid football cleats. The "
      "one-piece Flyknit upper is lightweight, supportive and fused to a "
      "durable skin layer to prevent your foot from sliding around as you "
      "change direction. A V-propulsion traction system on the carbon fiber "
      "outsole keeps you playing with power through its variable cleat "
      "heights around the forefoot."),
   price="$199.99",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "pTSA-20470244nm.jpg"),
   category=category2)
# Add item to database
session.add(item2)
session.commit()

#Create an item
item3 = Item(
   user_id=1,
   name="RIDDELL Youth Revolution Attack Football Helmet",
   description=("A great starter helmet for young players, the RIDDELL "
      "Revolution Attack comes equipped with Patented Side Impact Protection "
      "(PSIP) integrated into the shell for enhanced safety. Its fitted liner "
      "system is also incredibly stable and comfortable so they can stay "
      "focused on the ball and give the game their all."),
   price="$99.99",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "pTSA-20470244nm.jpg"),
   category=category2)
# Add item to database
session.add(item3)
session.commit()

#Create an item
item4 = Item(
   user_id=1,
   name="UNDER ARMOUR Adult ArmourFuse Chinstrap",
   description=("Make comfort as much of a priority as protection on the "
      "field with this UNDER ARMOUR ArmourFuse chinstrap! The super-tough "
      "nylon shell will keep you safe season after season, while a "
      "removable and washable internal foam pad features a gel insert for a "
      "cushioned fit. An ArmourFuse TPU overmold also absorbs shock and "
      "disperses impact."),
   price="$19.99",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "pTSA-14645414nm.jpg"),
   category=category2)
# Add item to database
session.add(item4)
session.commit()

#Create an item
item5 = Item(
   user_id=1,
   name="OAKLEY Football Helmet Clear Lens Shield", 
   description=("Football gladiators, protect your face on the gridiron with "
      "the OAKLEY football helmet clear lens shield. It offers "
      "distortion-free vision at every angle so you'll see your opponent "
      "clearly. The shield has anti-fog performance and scratch-resistant "
      "durability, along with impact-resistant Plutonite for maximum "
      "protection."),
   price="$50.00",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "pTSA-10103755nm.jpg"),
   category=category2)
# Add item to database
session.add(item5)
session.commit()

#Create an item
item6 = Item(
   user_id=1,
   name="Schutt Varsity Flex 2.0 All Purpose Football Shoulder Pads", 
   description=("The Schutt Varsity Flex 2.0 football shoulder pads are made "
      "to fit almost any player on the field. They feature a wider-cut "
      "design in the arch, which gives you complete range of motion and "
      "maximum versatility. EVA comfort foam delivers impact protection, "
      "while ventilated holes in the arch allow heat to escape and sweat to "
      "quickly evaporate."),
   price="$125.00",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "p16191511nm.jpg"),
   category=category2)
# Add item to database
session.add(item6)
session.commit()

#Create an item
item7 = Item(
   user_id=1,
   name=("NIKE Men's Pro Combat Hyperstrong 3.0 Compression:"
      " 4-Pad Football Top"), 
   description=("You'll be ready to take some hard hits in this NIKE men's "
      "Pro Combat Hyperstrong 3.0 compression 4-pad football top. It's "
      "crafted with stretchy Dri-FIT mesh that keeps you cool on the field "
      "and features NIKE De-Tech foam padding for the ultimate in impact "
      "resistance."),
   price="$89.00",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "pTSA-17059851nm.jpg"),
   category=category2)
# Add item to database
session.add(item7)
session.commit()

# Create our third category
category3 = Category(user_id=1,
   name="Basketball",
   img_url="https://encrypted-tbn1.gstatic.com/images?q=tbn:"
      "ANd9GcRkGCBMKil3owrchJj-G7_rseCbxGqQr03sLfqEwLR0FVtSys6Y1w")
# Add it to the database
session.add(category3)
session.commit()

#Create an item
item1 = Item(
   user_id=1,
   name="Spalding NBA 3-Pound Weighted Basketball",
   description=("This 3-pound weighted basketball from Spalding is perfect "
      "for maximizing your arm, wrist, and finger strength, with the goal of "
      "extending your shooting range. It bounces just like an NBA regulation "
      "ball and is designed for indoor use only."),
   price="$52.99",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "p20674267nm.jpg"),
   category=category3)
# Add item to database
session.add(item1)
session.commit()

#Create an item
item2 = Item(
   user_id=1,
   name="Nike Men's Kyrie 1 High Basketball Shoes", 
   description=("You'll be sinking shots like a pro in these Nike "
      "men's Kyrie 1 high-top basketball shoes. They're cushioned with "
      "responsive, lightweight Phylon foam that supports without adding "
      "unnecessary weight. The modified herringbone outsole provides "
      "excellent traction and durability, and wraps up the sides to give you "
      "extra grip and protection during the game."),
   price="$110.99",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "pTSA-20468825nm.jpg"),
   category=category3)
# Add item to database
session.add(item2)
session.commit()

#Create an item
item2 = Item(
   user_id=1,
   name=("Adidas Men's Golden State Warriors Stephen Curry Performance Road "
      "Replica Jersey"), 
   description=("At your last appointment, your doc said that you bleed "
      "Warriors' colors; now dress the part in this adidas men's Golden "
      "State Warriors Stephen Curry Performance road replica jersey! Its "
      "bold graphics help you declare allegiance to your beloved hoops team, "
      "all while giving a shout-out to the famous NBA point guard himself."),
   price="$79.99",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "pTSA-17141444nm.jpg"),
   category=category3)
# Add item to database
session.add(item2)
session.commit()

#Create an item
item3 = Item(
   user_id=1,
   name="Adidas Men's Golden State Warriors Klay Thompson #11 Jersey", 
   description=("Show your support for the other splash brother and now "
      "dress the part in this adidas men's Golden State Warriors Klay "
      "Thompson Performance road replica jersey! Its bold graphics help "
      "you declare allegiance to your beloved hoops team, all while giving a "
      "shout-out to the man with the sweet J."),
   price="$79.99",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "pTSA-19476792nm.jpg"),
   category=category3)
# Add item to database
session.add(item3)
session.commit()

#Create an item
item4 = Item(
   user_id=1,
   name="Nike Women's Pro Padded Sports Bra", 
   description=("With its compression fit, the Nike women's Pro padded "
      "sports bra offers the medium support you need while exercising. "
      "Dri-FIT technology wicks away sweat for total comfort, while "
      "flatlock seams prevent chafing. Removable pads provide flattering "
      "shaping and a little extra coverage."),
   price="$39.99",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "pTSA-18309756nm.jpg"),
   category=category3)
# Add item to database
session.add(item4)
session.commit()

#Create an item
item5 = Item(
   user_id=1,
   name="Nike Men's Elite Stripe Basketball Shorts", 
   description=("Attack the lane with confidence in the Nike men's Elite "
      "Stripe basketball shorts. They're built with a lightweight fabric "
      "and Dri-FIT sweat-wicking technology for a cooler, more comfortable "
      "feel. Contrast-color panels add an extra pop of style, and dual side "
      "pockets provide essential storage."),
   price="$45.99",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "pTSA-14759392nm.jpg"),
   category=category3)
# Add item to database
session.add(item5)
session.commit()

#Create an item
item6 = Item(
   user_id=1,
   name="EVOSHIELD Adult Compression Arm Sleeve", 
   description=("Stay loose and ready for the game with the EVOSHIELD adult "
      "compression arm sleeve. It provides muscle support to reduce fatigue "
      "while keeping your arm warm."),
   price="$13.99",
   img_url=("http://www.sportsauthority.com/graphics/product_images/"
      "pTSA-10785993nm.jpg"),
   category=category3)
# Add item to database
session.add(item6)
session.commit()


# Create our fourth category
category4 = Category(user_id=1,
   name="Snowboarding",
   img_url="https://encrypted-tbn3.gstatic.com/images?q=tbn:"
      "ANd9GcRCzytxcqNQcNIxe3K1kBx8s9Y8KNPVm1H_pMzwFcrY7s0AyY9JBQ")
# Add it to the database
session.add(category4)
session.commit()


# Create our fifth category
category5 = Category(user_id=1,
   name="Skiing",
   img_url="http://insuranceupdate.tk/wp-content/uploads/2015/11/110.jpg")
# Add it to the database
session.add(category5)
session.commit()


# Create our sixth category
category6 = Category(user_id=1,
   name="Hockey",
   img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:"
      "ANd9GcST1E2C-z39YEsU2mQcUMuqkwdHfO1X3SLIK6hUbKOpYJzpuKomjQ")
# Add it to the database
session.add(category6)
session.commit()

# DELETE THE BLOCK QUOTES TO ADD THE REST OF THE CATEGORIES

""" 
# Create our seventh category
category7 = Category(user_id=1, name="Baseball")
# Add it to the database
session.add(category7)
session.commit()


# Create our eigth category
category8 = Category(user_id=1, name="Rugby")
# Add it to the database
session.add(category8)
session.commit()


# Create our nineth category
category9 = Category(user_id=1, name="Golf")
# Add it to the database
session.add(category9)
session.commit()


# Create our tenth category
category10 = Category(user_id=1, name="LaCrosse")
# Add it to the database
session.add(category10)
session.commit()


# Create our eleventh category
category11 = Category(user_id=1, name="Ice Hockey")
# Add it to the database
session.add(category11)
session.commit()


# Create our twelveth category
category12 = Category(user_id=1, name="Tennis")
# Add it to the database
session.add(category12)
session.commit()


# Create our thirteenth category
category13 = Category(user_id=1, name="Swimming")
# Add it to the database
session.add(category13)
session.commit()


# Create our fourteenth category
category14 = Category(user_id=1, name="Track & Field")
# Add it to the database
session.add(category14)
session.commit()
"""


print "........................................"
print "Added items to database."
print "........................................"