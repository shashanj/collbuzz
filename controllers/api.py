# -*- coding: utf-8 -*-
# try something like

@request.restful()
def product():
	response.view = 'generic.json'
	def GET(*args,**vars):

		########### get items ##############
		if args[0] == 'all':
			if len(args) > 1  :
				upper_limit = 20+int(args[1])*20

				if upper_limit > db(db.sellinng_item).count():
					upper_limit =  db(db.sellinng_item).count()

				row = db(db.sellinng_item).select(limitby=(0+int(args[1])*20,upper_limit))

			else : 
				row = db(db.sellinng_item).select(limitby=(0,20))
			return dict(items = row)


		############ get a single item ##############
		if args[0].isdigit() :
			id = int(args[0])
			row = db(db.sellinng_item.id == id).select().first()
			return dict(item = row)


		########### search items ##############
		elif args[0] == 'search':
			try : 
				term = vars['q']
				row = db(db.sellinng_item.name.like('%'+term+'%') | db.sellinng_item.category.like ('%' + term +'%') | db.sellinng_item.sub_cat.like ('%' + term +'%') | db.sellinng_item.tags.like ('%' + term +'%')).select()			
				if len(row)==0:
					return dict(items = row, message = 'search returned 0 results')
				return dict(items = row, message = 'search complete')
			
			except : 
				return dict(items = {}, message = 'nothing to search')



		########### filter items ##############
		elif args[0] == 'filter':
			final = []
			try : 
				cat = request.get_vars.category
				queries=[]
				if isinstance(cat,list) :
					for category in cat:
						queries.append(db.sellinng_item.category == category)
				elif  isinstance(cat,str): 
					queries.append(db.sellinng_item.category == cat)
				
				final.append(reduce(lambda a,b : (a | b),queries))
			except :
				pass

			try : 		
				sub_category = vars['sub_category']
				queries=[]
				if  isinstance(sub_category,list):
					for subcategory in sub_category:
						queries.append(db.sellinng_item.sub_cat == subcategory)
				elif  isinstance(sub_category,str):
					queries.append(db.sellinng_item.sub_cat == sub_category)
				
				final.append(reduce(lambda a,b : (a | b),queries))
			except :
				pass

			try:
				min_amount = float(vars['min'])
				# final.append(db.sellinng_item.current_bid >= min_amount)
			except:
				pass

			try :
				max_amount = vars['max']
				# final.append(db.sellinng_item.current_bid <= max_amount)
			except :
				pass

			try :
				delivery = vars['delivery']
				if  isinstance(delivery,list):
					for deliv in delivery:
						queries.append(db.sellinng_item.delivery_type == deliv)
				elif isinstance(delivery,str):
					queries.append(db.sellinng_item.sub_cat == sub_category)
				final.append(reduce(lambda a,b : (a | b),queries))
			except :
				pass
			
			query = reduce(lambda a,b : (a & b),final)
			row = db(query)

			try :
				sort = vars['sortby']
				row = row.select(limitby=(0,20),orderby = 'sellinng_item.' + sort )

			except :
				row = row.select(limitby=(0,20))
				
			return dict(items = row)


	# @auth.requires_login()
	def POST(**vars):
		try :
			name = vars['name']
			name = name.lower()

			seller = db.user[vars['seller']]

			if seller is None:
				return dict(status=400, message='invalid user')

			cat = vars['category']
			sub_category = vars['sub_cat']

			bill = bool(vars['bill_av'])
			autolist =  bool(vars['autolist'])

			try : 
				amount = vars['orig_amnt']
				amount = float(amount)

				min_bid = vars['min_bid']
				min_bid = float(min_bid)

				max_bid = vars['max_bid']
				max_bid = float(max_bid)

				max_no_bids = vars['max_no_bids']
				max_no_bids = int(max_no_bids)
			except :
				return dict(status=400, message='invalid floating values')
				

			description = vars['descript']
			tags = vars['tags']

			last_date = vars['expires_on']

			try:
				image = vars['image']
			except:
				image = ''

			try:
				video = vars['video']
			except:
				video = ''

			lat = vars['lati']
			longi = vars['longi']

			mobile = seller.mobile

			delivery = vars['delivery_type']

			if max_bid < min_bid :
				return dict(status = '400',message = 'maximum bid cannot be less than minimum bid')

			db.sellinng_item.insert(name=name,
				seller = seller,
				category = cat,
				sub_cat = sub_category,
				bill_av = bill,
				autolist = autolist,
				min_bid = min_bid,
				max_bid = max_bid,
				descript = description,
				tags = tags,
				orig_amnt = amount,
				mobile = mobile,
				expires_on = last_date,
				delivery_type = delivery,
				max_no_bids = max_no_bids,
				image = image,
				video = video,
				lati = lat,
				longi = longi,
			) 


			return dict(status = '201',message = 'item created')

		except : 
			return dict(status = '400',message = 'incomplete application')

	# @auth.requires_login()
	def PUT(record_id,**vars):
		db(db.sellinng_item.id==record_id).update(**vars)
		return dict(status = '200',message = 'item updated')

	def DELETE(table_name,record_id):

		return dict(status='403',message='forbidden')

	return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)


@request.restful()
def comment():
	response.view = 'generic.json'
	def GET(*args,**vars):

		########### get comments ##############
		if args[0] == 'all':
			if len(args) > 1  :
				upper_limit = 20+int(args[1])*20

				if upper_limit > db(db.item_comment).count():
					upper_limit =  db(db.item_comment).count()

				row = db(db.item_comment).select(limitby=(0+int(args[1])*20,upper_limit))

			else : 
				row = db(db.item_comment).select(limitby=(0,20))
			return dict(items = row)

	def POST(**vars):
		try :
			comment = vars['comment']
			item = db.sellinng_item[int(vars['item'])]
			comment_by = db.users(int(vars['comment_by']))

			db.item_comment.insert( comment = comment,
				item = item,
				comment_by = comment_by
			)

			return dict(status = '201',message = 'comment created')

		except :
			return dict(status = '400',message = 'incomplete application')

	# @auth.requires_login()
	def PUT(record_id,**vars):
		db(db.item_comment.id==record_id).update(**vars)
		return dict(status = '200',message = 'comment updated')

	# @auth.requires_login()
	def DELETE(record_id):
		db(db.item_comment.id==record_id).delete()
		return dict(status='200',message='comment deleted')

	return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)


@request.restful()
def getUserId():
	response.view = 'generic.json'
	def GET(*args,**vars):
		username = vars['username']

		row = db(db.user.username == username).select().first()
		id = row.id
		return dict(id = id)

	def POST(**vars):
		pass

	def PUT(record_id,**vars):
		pass

	def DELETE(record_id):
		pass

	return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)

@request.restful()
def getUserDetail():
	response.view = 'generic.json'
	def GET(user_id):

		row = db(db.user.id == user_id).select().first()
		return dict(user = row)

	def POST(**vars):
		pass

	def PUT(record_id,**vars):
		pass

	def DELETE(record_id):
		pass

	return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)