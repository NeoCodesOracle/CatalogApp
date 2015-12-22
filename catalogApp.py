from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from catalog_database import Base, User, Category, Item

# IMPORTS FOR API ENDPOINTS
from flask import jsonify

# IMPORTS FOR SESSION MANAGEMENT
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# IMPORTS FOR DECORATOR
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "CatalogApp"


engine = create_engine('sqlite:///catalog.db')

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    '''
    Connects a user using her Facebook credentials.
    '''
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_\
           type=fb_exchange_token&client_id=%s&client_secret=%s&\
           fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly
    # logout, let's strip out the information before the equals sign
    # in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200\
            &width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 150px; height: 150px;border-radius: 150px;\
                -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    '''
    Disconnects a user from Facebook.
    '''
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com\
            /%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    '''
    Connects a user using her Google account.
    '''
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 150px; height: 150px;border-radius: \
                            150px;-webkit-border-radius: 150px;\
                            -moz-border-radius: 150px;"> '
    flash("Now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    '''
    Disconnects a user from her Google account.
    '''
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['credentials']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    '''
    Disconnects a user based on login provider.
    '''
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCategories'))


# User Helper Functions
def createUser(login_session):
    '''
    Creates a new user from login_session credentials.
    '''
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], img_url=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    '''
    Looks up a user given user_id and returns user if found.
    '''
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    '''
    Returns the user_id of the user matching email address.
    '''
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/login')
def showLogin():
    '''
    Renders the page for login.
    '''
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # RENDER LOGIN TEMPLATE
    return render_template('newlogin.html', STATE=state,
                           login_session=login_session)


# Decorator function to require login
def login_required(f):
    """
    Decorator function -- forces user to login by redirecting to login page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in login_session:
            return redirect(url_for('showLogin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# JSON APIs to view Category Information
@app.route('/categories/<int:category_id>/categoryItems/JSON')
def categoryItemsJSON(category_id):
    '''
    Returns JSON objects for all items matching category_id
    '''
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category.id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/category/<int:category_id>/item/<int:item_id>/JSON')
def categoryItemJSON(category_id, item_id):
    '''
    Returns JSON representation for a single item matching item_id
    '''
    category_item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=category_item.serialize)


@app.route('/categories/JSON')
def categoriesJSON():
    '''
    Returns JSON objects for all categories in catalog.
    '''
    categories = session.query(Category).all()
    return jsonify(Catergories=[c.serialize for c in categories])
# END JSON APIs


# XML ENDPOINTS
@app.route('/categories/items/XML')
def allItemsXML():
    '''
    Returns XML objects for all items in catalog.
    '''
    items = session.query(Item).all()
    return render_template('items.xml', items=items)
# END XML ENDPOINTS


@app.route('/')
@app.route('/categories/')
def showCategories():
    '''
    Shows all the categories in database by alphabetical order.
    '''
    categories = session.query(Category).order_by(asc(Category.name))
    if 'username' not in login_session:
        return render_template('guestcategories.html', categories=categories,
                               login_session=login_session)
    else:
        return render_template('categories.html', categories=categories,
                               login_session=login_session)


@app.route('/categories/new/', methods=['GET', 'POST'])
@login_required
def addCategory():
    '''
    Adds a new category to the existing database.
    '''
    if request.method == 'POST':
        if request.form['name']:
            newCategory = Category(name=request.form['name'],
                                   img_url=request.form['img_url'],
                                   user_id=login_session['user_id'])
            session.add(newCategory)
            session.commit()
        flash("You added a new category to the catalog.")
        return redirect(url_for('showCategories',
                                login_session=login_session))
    else:
        return render_template('newcategory.html',
                               login_session=login_session)


@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
@login_required
def editCategory(category_id):
    '''
    Makes changes to an existing category in the database.
    '''
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    if editedCategory.user_id != login_session['user_id']:
        flash("You cannot edit this category. Catergories can only be \
              modified by their owners. Create a category of your own to \
              modify.")
        return redirect(url_for('showCategories'))
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
        if request.form['img_url']:
            editedCategory.img_url = request.form['img_url']
        session.add(editedCategory)
        session.commit()
        flash("You have made changes to a category.")
        return redirect(url_for('showCategories'))
    else:
        return render_template('editcategory.html', category=editedCategory,
                               login_session=login_session)


@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
@login_required
def deleteCategory(category_id):
    '''
    Removes an existing category from the database.
    '''
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()
    if categoryToDelete.user_id != login_session['user_id']:
        flash("You cannot delete this category. Catergories can only be \
              deleted by their owners.")
        return redirect(url_for('showCategories'))
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        flash("You have deleted a category.")
        return redirect(url_for('showCategories'))
    else:
        return render_template('deletecategory.html',
                               category=categoryToDelete,
                               login_session=login_session)


@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/show')
def showItems(category_id):
    '''
    Shows all the items that belong to category matching category_id.
    '''
    categoryToShow = session.query(Category).filter_by(
        id=category_id).one()
    categoryItems = session.query(Item).filter_by(
        category_id=category_id).order_by(asc(Item.name))
    return render_template('showitems.html',
                           category=categoryToShow,
                           items=categoryItems,
                           login_session=login_session)


@app.route('/categories/<int:newItemCategory_id>/new/',
           methods=['GET', 'POST'])
@login_required
def addItem(newItemCategory_id):
    '''
    Adds an item to category matching newItemCategory_id.
    '''
    category = session.query(Category).filter_by(
        id=newItemCategory_id).one()
    if login_session['user_id'] != category.user_id:
        flash("Only the owner of %s category may add an item to it."
              % category.name)
        return redirect(url_for('showItems', category_id=category.id))
    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            img_url=request.form['img_url'],
            category_id=category.id,
            user_id=category.user_id)
        session.add(newItem)
        session.commit()
        flash("A new item has been added to this category.")
        return redirect(url_for('showItems', category_id=category.id))
    else:
        return render_template('newitem.html', category=category,
                               login_session=login_session)


@app.route('/categories/<int:category_id>/<int:item_id>/edit/',
           methods=['GET', 'POST'])
@login_required
def editItem(category_id, item_id):
    '''
    Edits item with matching item_id.
    '''
    itemToEdit = session.query(Item).filter_by(id=item_id).one()
    belongsToCategory = session.query(Category).filter_by(
        id=itemToEdit.category_id).one()
    if login_session['user_id'] != itemToEdit.user_id:
        flash("Only the owner of %s category may edit this item."
              % belongsToCategory.name)
        return redirect(url_for('showItems', category_id=belongsToCategory.id))
    if request.method == 'POST':
        if request.form['name']:
            itemToEdit.name = request.form['name']
        if request.form['price']:
            itemToEdit.price = request.form['price']
        if request.form['description']:
            itemToEdit.description = request.form['description']
        if request.form['img_url']:
            itemToEdit.img_url = request.form['img_url']
        session.add(itemToEdit)
        session.commit()
        flash("You have made changes to an item in this category.")
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('edititem.html', item=itemToEdit,
                               login_session=login_session)


@app.route('/categories/<int:category_id>/<int:item_id>/delete/',
           methods=['GET', 'POST'])
@login_required
def deleteItem(category_id, item_id):
    '''
    Removes item matching item_id from database.
    '''
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    belongsToCategory = session.query(Category).filter_by(
        id=category_id).one()
    if login_session['user_id'] != itemToDelete.user_id:
        flash("Only the owner of %s category may remove this item."
              % belongsToCategory.name)
        return redirect(url_for('showItems', category_id=category_id))
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("You have removed an item in this category.")
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('deleteitem.html', item=itemToDelete,
                               login_session=login_session)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
