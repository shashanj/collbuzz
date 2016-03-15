# Here define general models apart from user and few essential models

db.define_table('sellinng_item',
	Field('name'),
	Field('seller'),
	Field('category'),
	Field('sub_cat'),
	Field('bill_av','boolean'), # weather bill is availaible or not
	Field('min_bid'),
	Field('max_bid'),
	Field('view_count','integer',default=0),
	Field('status','integer'), # Item sold status- can be 0,1,2,3, etc for sold, hot , deleted , etc.. 
	Field('image'), # Will be string, storing multiple image names only 

	format="%(name)s"
)

db.define_table('item_bid',
	Field('bidder'),
	Field('sellinng_item_id'),
	Field('amount'),
	Field('status'), 	#status of bid, 0,1,2, etc.. it's seen, accepted,rejected etc...
	
	)

