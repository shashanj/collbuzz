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

