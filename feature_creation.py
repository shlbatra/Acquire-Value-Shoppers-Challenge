# -*- coding: utf-8 -*-
"""
Created on Sat Nov 08 19:17:39 2014

@author: Shankar
"""

# -*- coding: UTF-8 -*-

from datetime import datetime

loc_offers = "G:\\Marketing_project\\Repear_Buyers\\Datasets\\Sampled Data\\Model\\offers.csv"
loc_transactions = "G:\\Marketing_project\\Repear_Buyers\\Datasets\\Sampled Data\\Model\\CustModelTrans1.csv"
loc_train = "G:\\Marketing_project\\Repear_Buyers\\Datasets\\Sampled Data\\Model\\trainHistoryFinal.csv"
loc_test = "G:\\Marketing_project\\Repear_Buyers\\Datasets\\Sampled Data\\Model\\testHistoryFinal.csv"

# will be created
#loc_reduced = "data/reduced.csv" 
loc_out_train = "G:\\Marketing_project\\Repear_Buyers\\Datasets\\Sampled Data\\Model\\train.csv"
loc_out_test = "G:\\Marketing_project\\Repear_Buyers\\Datasets\\Sampled Data\\Model\\test.csv"

def diff_days(s1,s2):
	date_format = "%Y-%m-%d"
	a = datetime.strptime(s1, date_format)
	b = datetime.strptime(s2, date_format)
	delta = b - a
	return delta.days

def feature():
	features = {}
	features['custid'] = 0
	features['label'] = 0
	features['total_spend'] = 0.0

	# Offer attributes
	features['offer_value'] = 0.0
	features['offer_quantity'] = 0.0

	#Company level features
	features['has_bought_company'] = 0.0
	features['has_bought_company_q'] = 0.0
	features['has_bought_company_a'] = 0.0
	features['has_bought_company_30'] = 0.0
	features['has_bought_company_q_30'] = 0.0
	features['has_bought_company_a_30'] = 0.0
	features['has_bought_company_60'] = 0.0
	features['has_bought_company_q_60'] = 0.0
	features['has_bought_company_a_60'] = 0.0
	features['has_bought_company_90'] = 0.0
	features['has_bought_company_q_90'] = 0.0
	features['has_bought_company_a_90'] = 0.0
	features['has_bought_company_180'] = 0.0
	features['has_bought_company_q_180'] = 0.0
	features['has_bought_company_a_180'] = 0.0

	#Category level features
	features['has_bought_category'] = 0.0
	features['has_bought_category_q'] = 0.0
	features['has_bought_category_a'] = 0.0
	features['has_bought_category_30'] = 0.0
	features['has_bought_category_q_30'] = 0.0
	features['has_bought_category_a_30'] = 0.0
	features['has_bought_category_60'] = 0.0
	features['has_bought_category_q_60'] = 0.0
	features['has_bought_category_a_60'] = 0.0
	features['has_bought_category_90'] = 0.0
	features['has_bought_category_q_90'] = 0.0
	features['has_bought_category_a_90'] = 0.0
	features['has_bought_category_180'] = 0.0
	features['has_bought_category_q_180'] = 0.0
	features['has_bought_category_a_180'] = 0.0
	
	#Brand level features
	features['has_bought_brand'] = 0.0
	features['has_bought_brand_q'] = 0.0
	features['has_bought_brand_a'] = 0.0
	features['has_bought_brand_30'] = 0.0
	features['has_bought_brand_q_30'] = 0.0
	features['has_bought_brand_a_30'] = 0.0
	features['has_bought_brand_60'] = 0.0
	features['has_bought_brand_q_60'] = 0.0
	features['has_bought_brand_a_60'] = 0.0
	features['has_bought_brand_90'] = 0.0
	features['has_bought_brand_q_90'] = 0.0
	features['has_bought_brand_a_90'] = 0.0
	features['has_bought_brand_180'] = 0.0
	features['has_bought_brand_q_180'] = 0.0
	features['has_bought_brand_a_180'] = 0.0

	return features
	
#keep a dictionary with the offerdata
offers = {}
for e, line in enumerate( open(loc_offers) ):
	row = line.strip().split(",")
	offers[ row[0] ] = row

#keep two dictionaries with the shopper id's from test and train
train_ids = {}
test_ids = {}
for e, line in enumerate( open(loc_train) ):
	if e > 0:
		row = line.strip().split(",")
		train_ids[row[0]] = row
for e, line in enumerate( open(loc_test) ):
	if e > 0:
		row = line.strip().split(",")
		test_ids[row[0]] = row

#open two output files
with open(loc_out_train, "wb") as out_train, open(loc_out_test, "wb") as out_test:
	#iterate through reduced dataset 
	last_id = 0
	
	#Defining empty feature space
	features = feature()
	
	test = False
		
	ColumnList = ''
	for k, v in features.items():
		ColumnList += ',' + str(k)
	out_train.write( ColumnList )
	out_test.write( ColumnList )
	
	for e, line in enumerate( open(loc_transactions) ):
		if e > 0: #skip header
			row = line.strip().split(",")
			#write away the features when we get to a new shopper id
			if last_id != row[0] and e != 1:
					outline = ""
					features['custid'] = last_id
					for k, v in features.items():
						if v == 0:
							outline += ',' + str(0)
						else:
							outline += ',' + str(v)
					outline += "\n"
					last_outline = outline
					last_features = features

					if last_id in test_ids:
						out_test.write( outline )
					elif last_id in train_ids:
						out_train.write( outline )

					#print "Writing features or storing them in an array"
					#reset features
					features = feature()

				#generate features from transaction record
				#check if we have a test sample or train sample
			if row[0] in train_ids or row[0] in test_ids:
				#generate label and history
				if row[0] in train_ids:
					history = train_ids[row[0]]
					test = False
					if train_ids[row[0]][5] == "t":
						features['label'] = 1
					else:
						features['label'] = 0
				else:
					history = test_ids[row[0]]
					test = True
					if test_ids[row[0]][5] == "t":
						features['label'] = 1
					else:
						features['label'] = 0


				#print "label", label 
				#print "trainhistory", train_ids[row[0]]
				#print "transaction", row
				#print "offers", offers[ train_ids[row[0]][2] ]
				#print
				
				features['offer_value'] = offers[ history[2] ][4]
				features['offer_quantity'] = offers[ history[2] ][2]
				offervalue = offers[ history[2] ][4]
				
				features['total_spend'] += float( row[10] )
				
				if offers[ history[2] ][3] == row[4]:
					features['has_bought_company'] += 1.0
					features['has_bought_company_q'] += float( row[9] )
					features['has_bought_company_a'] += float( row[10] )
					
					date_diff_days = diff_days(row[6],history[-1])
					if date_diff_days < 30:
						features['has_bought_company_30'] += 1.0
						features['has_bought_company_q_30'] += float( row[9] )
						features['has_bought_company_a_30'] += float( row[10] )
					if date_diff_days < 60:
						features['has_bought_company_60'] += 1.0
						features['has_bought_company_q_60'] += float( row[9] )
						features['has_bought_company_a_60'] += float( row[10] )
					if date_diff_days < 90:
						features['has_bought_company_90'] += 1.0
						features['has_bought_company_q_90'] += float( row[9] )
						features['has_bought_company_a_90'] += float( row[10] )
					if date_diff_days < 180:
						features['has_bought_company_180'] += 1.0
						features['has_bought_company_q_180'] += float( row[9] )
						features['has_bought_company_a_180'] += float( row[10] )
				
				if offers[ history[2] ][1] == row[3]:
					features['has_bought_category'] += 1.0
					features['has_bought_category_q'] += float( row[9] )
					features['has_bought_category_a'] += float( row[10] )
					date_diff_days = diff_days(row[6],history[-1])
					if date_diff_days < 30:
						features['has_bought_category_30'] += 1.0
						features['has_bought_category_q_30'] += float( row[9] )
						features['has_bought_category_a_30'] += float( row[10] )
					if date_diff_days < 60:
						features['has_bought_category_60'] += 1.0
						features['has_bought_category_q_60'] += float( row[9] )
						features['has_bought_category_a_60'] += float( row[10] )
					if date_diff_days < 90:
						features['has_bought_category_90'] += 1.0
						features['has_bought_category_q_90'] += float( row[9] )
						features['has_bought_category_a_90'] += float( row[10] )						
					if date_diff_days < 180:
						features['has_bought_category_180'] += 1.0
						features['has_bought_category_q_180'] += float( row[9] )
						features['has_bought_category_a_180'] += float( row[10] )				
				if offers[ history[2] ][5] == row[5]:
					features['has_bought_brand'] += 1.0
					features['has_bought_brand_q'] += float( row[9] )
					features['has_bought_brand_a'] += float( row[10] )
					date_diff_days = diff_days(row[6],history[-1])
					if date_diff_days < 30:
						features['has_bought_brand_30'] += 1.0
						features['has_bought_brand_q_30'] += float( row[9] )
						features['has_bought_brand_a_30'] += float( row[10] )
					if date_diff_days < 60:
						features['has_bought_brand_60'] += 1.0
						features['has_bought_brand_q_60'] += float( row[9] )
						features['has_bought_brand_a_60'] += float( row[10] )
					if date_diff_days < 90:
						features['has_bought_brand_90'] += 1.0
						features['has_bought_brand_q_90'] += float( row[9] )
						features['has_bought_brand_a_90'] += float( row[10] )						
					if date_diff_days < 180:
						features['has_bought_brand_180'] += 1.0
						features['has_bought_brand_q_180'] += float( row[9] )
						features['has_bought_brand_a_180'] += float( row[10] )	
			last_id = row[0]
			if e % 100000 == 0:
				print e
