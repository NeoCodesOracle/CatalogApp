from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from catalog_database import Base, User, Category, Item

# IMPORTS FOR SESSION MANAGEMENT
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "CatalogApp"


engine=create_engine('sqlite:///catalog.db')

DBSession=sessionmaker(bind=engine)
session=DBSession()


@app.route('/gconnect', methods=['POST'])
def gconnect():
	'''Allows user to signin using Google account'''
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
	# access_token = login_session.get('credentials')
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
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
		response = make_response(
			json.dumps('Current user is already connected.'), 200)
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
	output += ' " style = "width: 200px; height: 200px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
	flash("You are now logged in as %s" % login_session['username'])
	print "done!"
	return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], img_url=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/login')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits)
		for x in xrange(32))
	login_session['state'] = state
	# RENDER LOGIN TEMPLATE
	return render_template('login.html', STATE=state)

# JSON APIs to view Category Information
@app.route('/categories/<int:category_id>/categoryItems/JSON')
def categoryItemsJSON(category_id):
    '''Returns JSON objects for all items matching category_id'''	
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category.id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/category/<int:category_id>/item/<int:item_id>/JSON')
def categoryItemJSON(category_id, item_id):
	'''Returns JSON representation for a single item matching item_id'''
	category_item = session.query(Item).filter_by(id=item_id).one()
	return jsonify(Item=category_item.serialize)


@app.route('/categories/JSON')
def categoriesJSON():
	'''Returns JSON objects for all categories in catalog'''
	categories = session.query(Category).all()
	return jsonify(Catergories=[c.serialize for c in categories])
# END JSON APIs


@app.route('/')
@app.route('/categories/')
def showCategories():
	'''Shows all the categories in database.'''
	categories=session.query(Category).order_by(asc(Category.name))
	return render_template('categories.html', categories=categories)


@app.route('/categories/new/', methods=['GET', 'POST'])
def addCategory():
	'''Adds a new category to the existing database.'''
	if request.method == 'POST':
		newCategory=Category(name=request.form['name'], img_url=
			request.form['img_url'])
		session.add(newCategory)
		session.commit()
		flash("You added a new category to the catalog.")
		return redirect(url_for('showCategories'))
	else:
		return render_template('newcategory.html')


@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
	'''Makes changes to an existing category in the database.'''
	editedCategory=session.query(Category).filter_by(id=category_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedCategory.name=request.form['name']
		if request.form['img_url']:
			editedCategory.img_url=request.form['img_url']
		session.add(editedCategory)
		session.commit()
		flash("You have made changes to a category.")
		return redirect(url_for('showCategories'))
	else:
		return render_template('editcategory.html', category=editedCategory)


@app.route('/categories/<int:category_id>/delete/', methods=['GET','POST'])
def deleteCategory(category_id):
	'''Removes an existing category from the database.'''
	categoryToDelete=session.query(Category).filter_by(id=category_id).one()
	if request.method == 'POST':
		session.delete(categoryToDelete)
		session.commit()
		flash("You have deleted a category.")
		return redirect(url_for('showCategories'))
	else:
		return render_template('deletecategory.html',
			category=categoryToDelete)


@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/show')
def showItems(category_id):
	'''Shows all the items that belong to category matching category_id.'''
	categoryToShow=session.query(Category).filter_by(
		id=category_id).one()
	categoryItems=session.query(Item).filter_by(
		category_id=category_id).order_by(asc(Item.name))
	return render_template('showitems.html', category=categoryToShow,
		items=categoryItems)


@app.route('/categories/<int:newItemCategory_id>/new/',
	methods=['GET','POST'])
def addItem(newItemCategory_id):
	'''Adds an item to category matching newItemCategory_id.'''
	categoryToShow=session.query(Category).filter_by(
		id=newItemCategory_id).one()
	if request.method == 'POST':
		newItem=Item(
			name=request.form['name'],
			description=request.form['description'],
			price=request.form['price'],
			img_url=request.form['img_url'],
			category_id=categoryToShow.id)
		session.add(newItem)
		session.commit()
		flash("A new item has been added to this category.")
		return redirect(url_for('showItems', category_id=categoryToShow.id))
	else:
		return render_template('newitem.html', category=categoryToShow)


@app.route('/categories/<int:category_id>/<int:item_id>/edit/',
	methods=['GET','POST'])
def editItem(category_id, item_id):
	'''Edits item with matching item_id.'''
	itemToEdit=session.query(Item).filter_by(id=item_id).one()
	belongsToCategory=session.query(Category).filter_by(
		id=itemToEdit.category_id).one()
	if request.method == 'POST':
		if request.form['name']:
			itemToEdit.name=request.form['name']
		if request.form['price']:
			itemToEdit.price=request.form['price']
		if request.form['description']:
			itemToEdit.description=request.form['description']
		if request.form['img_url']:
			itemToEdit.img_url=request.form['img_url']
		session.add(itemToEdit)
		session.commit()
		flash("You have made changes to an item in this category.")
		return redirect(url_for('showItems', category_id=category_id))
	else:
		return render_template('edititem.html', item=itemToEdit)


@app.route('/categories/<int:category_id>/<int:item_id>/delete/',
	methods=['GET','POST'])
def deleteItem(category_id, item_id):
	'''Removes item matching item_id from database.'''
	itemToDelete=session.query(Item).filter_by(id=item_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash("You have removed an item in this category.")
		return redirect(url_for('showItems', category_id=category_id))
	else:
		return render_template('deleteitem.html', item=itemToDelete)


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
