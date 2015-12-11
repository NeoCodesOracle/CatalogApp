from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from catalog_database import Base, User, Category, Item

# IMPORTS FOR SESSION MANAGEMENT
from flask import session as login_session
import random, string

engine=create_engine('sqlite:///catalog.db')

DBSession=sessionmaker(bind=engine)
session=DBSession()


@app.route('/login')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits)
		for x in xrange(32))
	login_session['state'] = state
	# RENDER LOGIN TEMPLATE
	return render_template('login.html')

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
