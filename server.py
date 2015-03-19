from models import *

db.create_all()

@app.route('/dataControl/insertData')
def insertData(account, recentUrl, word, mean, deleteCheck):
	account = account
	recentUrl = recentUrl
	word = word
	mean = mean
	deleteCheck = deleteCheck


	namnam = User(account, recentUrl, word, mean, deleteCheck)

	try:
		db.session.add(namnam)
		db.session.commit()
	except:
		db.session.rollback()
	finally:
		db.session.close()

	users = User.query.all()
	# admin = User.query.filter_by(username='haha').all()
	select = User.query.filter_by(account = 'd').all()
	print users

	print '====================='
	print select

@app.route('/dataControl/updateData')
def updateData():

	return users

if __name__ == '__main__':
	app.run()