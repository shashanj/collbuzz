# -*- coding: utf-8 -*-
# try something like
@request.restful()
def api():
	response.view = 'generic.json'
	def GET(*args,**vars):
		patterns = [
			"/user[user]",
			"/user/id/{user.id}",
			"/user/id/{user.id}/:field",

			"/product[sellinng_item]",
			"/product/id/{sellinng_item.id}",
			"/product/id/{sellinng_item.id}/:field",
		]

		parser = db.parse_as_rest(patterns,args,vars)
		if parser.status == 200:
			return dict(content=parser.response)
		else :
			raise HTTP(parser.status,parser.error)

	def POST(table_name,**vars):
		return db[table_name].validate_and_insert(**vars)

	def PUT(table_name,record_id,**vars):
		return db(db[table_name]._id==record_id).update(**vars)

	def DELETE(table_name,record_id):
		return db(db[table_name]._id==record_id).delete()

	return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)

@request.restful()
def search():
	response.view = 'generic.json'
	def GET(*args,**vars):
		term = str(args[0])
		row = db(db.sellinng_item.name.like('%'+term+'%') | db.sellinng_item.category.like ('%' + term +'%') | db.sellinng_item.sub_cat.like ('%' + term +'%')).select()
		return dict(items = row)
	def POST(table_name,**vars):
		raise HTTP(400,'reached unknown territory')

	def PUT(table_name,record_id,**vars):
		raise HTTP(400,'reached unknown territory')

	def DELETE(table_name,record_id):
		raise HTTP(400,'reached unknown territory')

	return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)

@request.restful()
def filter():
	def GET(*args,**vars):
		response.view = 'generic.json'
		category = args[0]
		sort =  args[1]
		ship_to_you = args[2] # not understood and not available from database
		destination = args[3] # would be clear if above is clear
		free_shipping = args[4] # not available from database
		local_pickup = args[5] 
		# location - not understood
		digital_delivery = args[6] #  not understood
		if category != '0':
			row = db(db.sellinng_item.category == category)
		else :
			row = db(db.sellinng_item.id > 0)
		if local_pickup != '0':
			row = db(row.sellinng_item.delivery_type == 'local pickup')

		row = row.select(orderby = 'sellinng_item.' + sort)

		return dict(items = row)

	def POST(table_name,**vars):
		raise HTTP(400,'reached unknown territory')

	def PUT(table_name,record_id,**vars):
		raise HTTP(400,'reached unknown territory')

	def DELETE(table_name,record_id):
		raise HTTP(400,'reached unknown territory')

	return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)
