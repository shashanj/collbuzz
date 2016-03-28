# Here define general models apart from user and few essential models

db.define_table('sellinng_item',
	Field('name','string'),
	Field('seller','reference user'),
	Field('category','string'),
	Field('sub_cat','string'),
	Field('bill_av','boolean'), # weather bill is availaible or not
	Field('min_bid','double'),
	Field('max_bid','double'),
	Field('current_bid','double'),
	Field('current_bid_user','reference user'),
	Field('descript','text'),
	Field('tags','string'),
	Field('orig_amnt','double'),
	Field('mobile','string',length=10),
	Field('expires_on','date'),
	Field('pr_amnt','double'),
	Field('pr_till','date'),
	Field('delivery_type','string'),
	Field('max_no_bids','integer'),
	Field('view_count','integer',default=0),
	Field('like_count','integer',default=0),
	Field('bid_count','integer',default=0),
	Field('type','string'), # Premium, Hot etc... 
	Field('status','integer'), # Item sold status- can be 0,1,2,3, etc for sold, hot , deleted , etc.. 
	Field('image','string'), # Will be string, storing multiple image names only 
	Field('video','string'),
	Field('flag','integer'),
	Field('need_rev'), # Needs review
	Field('lati','string'),
	Field('longi','string'),
	Field('autolist','boolean'),
	Field('list_fee','string'),
	Field('trans_fee','string'),
	format="%(name)s"
)

db.define_table('item_bid',
	Field('bidder','reference user'),
	Field('bid_item','reference sellinng_item'),
	Field('amount','double'),
	Field('status','string'), 	#status of bid, 0,1,2, etc.. it's seen, accepted,rejected,outbidded etc...
)

db.define_table('tasks',
	Field('body','text'), # sort of eligilbility
	Field('state','boolean',default=False), # task within the crdit completed 
)

db.define_table('credits',
	Field('name','string'),
	Field('reward','integer'), # amount of reward
	Field('tasks','list:reference tasks'), # many to one relation with tasks
	Field('started_on','datetime'),
	Field('ends_on','datetime'),
	Field('active','boolean'), # instead of delete use to deactivate the credit in between
	Field('timestamp','datetime',default=request.now,writable=False,readable=False),
)

db.define_table('user_credits', # mapping user for credits they want to score
	Field('user','reference user'),
	Field('credit','reference credits'),
	Field('status', 'string'), # complete, in progres , 
	format="%(name)s",
)

db.define_table('item_comment',
	Field('comment','text'),
	Field('item','reference sellinng_item'),
	Field('comment_by','reference user'),
	Field('replies','list:reference comment_reply'),
	Field('like','integer',default=0),
	Field('dislike','integer',default=0),
	Field('timestamp','datetime',default=request.now),
)

db.define_table('comment_reply',
	Field('reply','text'),
	Field('item','reference sellinng_item'),
	Field('reply_by','reference user'),
	Field('like','integer',default=0),
	Field('dislike','integer',default=0),
	Field('timestamp','datetime',default=request.now),
)

db.define_table('flag_reason',
	Field('body','string'),
)

db.define_table('flag_ad',
	Field('item','reference sellinng_item'),
	Field('flagged_by','reference user'),
	Field('reason','reference flag_reason'),
	Field('timestamp','datetime',default=request.now),
)

db.define_table('shortlist',
	Field('user','reference user'),
	Field('item', 'list:reference sellinng_item'),
)