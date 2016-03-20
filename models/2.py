# Here define general models apart from user and few essential models

db.define_table('sellinng_item',
	Field('name'),
	Field('seller'),
	Field('category'),
	Field('sub_cat'),
	Field('bill_av','boolean'), # weather bill is availaible or not
	Field('min_bid'),
	Field('max_bid'),
	Field('current_bid'),
	Field('current_bid_user'),
	Field('descript'),
	Field('tags'),
	Field('orig_amnt'),
	Field('mobile'),
	Field('expires_on'),
	Field('pr_amnt'),
	Field('pr_till'),
	Field('delivery_type'),
	Field('max_no_bids'),
	Field('view_count','integer',default=0),
	Field('like_count','integer',default=0),
	Field('bid_count','integer',default=0),
	Field('type'), # Premium, Hot etc... 
	Field('status','integer'), # Item sold status- can be 0,1,2,3, etc for sold, hot , deleted , etc.. 
	Field('image'), # Will be string, storing multiple image names only 
	Field('video'),
	Field('flag'),
	Field('need_rev'), # Needs review
	Field('lati'),
	Field('longi'),
	Field('autolist'),
	Field('list_fee'),
	Field('trans_fee'),
	format="%(name)s"
)

db.define_table('item_bid',
	Field('bidder'),
	Field('bid_item'),
	Field('amount'),
	Field('status'), 	#status of bid, 0,1,2, etc.. it's seen, accepted,rejected,outbidded etc...
)

