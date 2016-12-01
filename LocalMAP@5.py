from __future__ import division
import pandas as pd
import CFAlgorithms
import CBAlgorithms
import ValidationAlgorithm as va

# Importing all the files needed
cols = ['user_id', 'item_id', 'interaction']
interactions = pd.read_csv('TestDataSet/trainingSet.csv', sep='\t', names=cols, header=0)

items = pd.read_csv('DataSet/item_profile.csv', sep='\t', header=0)
active_items = items[(items.active_during_test == 1)]
active_items_idx = active_items[['item_id', 'active_during_test']]

# Dictionary with only active items
active_items_to_recommend = {}
for item, state in active_items_idx.values:
    active_items_to_recommend[item] = state

target_users = pd.read_csv('DataSet/target_users.csv')

CF_UB_similarity_shrink = 10
CF_UB_prediction_shrink = 10

CF_IB_similarity_shrink = 20
CF_IB_prediction_shrink = 10

CF_User_Rank_Weight = 0.5
CF_Item_Rank_Weight = 4

CF_Hybrid_KNN = 30
CF_Hybrid_Weight = 0.4

users_interactions_dictionary = {}

# Dictionaries for Content Based Algorithms
CB_user_items_dictionary = {}
CB_item_users_dictionary = {}

# Dictionaries for Collaborative Filtering Algorithms
CF_user_items_dictionary = {}
CF_item_users_dictionary = {}

# Create the dictionaries needed to compute the similarity between users or items
# It is the User Rating Matrix build with dictionaries
# Dictionary is a list of elements, each element is defined as following
# dict {user -> (list of {item -> interaction})}
print ("Create dictionaries for users and items")
for user, item, interaction in interactions.values:
    CF_user_items_dictionary.setdefault(user, {})[item] = 1 #int(interaction)

# dict {item -> (list of {user -> interaction})}
for user, item, interaction in interactions.values:
    CF_item_users_dictionary.setdefault(item, {})[user] = 1 #int(interaction)

# Compute the User-User Similarity for Collaborative Filtering User Based
CF_user_user_similarity_dictionary = CFAlgorithms.CFUserUserSimilarity(CF_user_items_dictionary, CF_item_users_dictionary,
                                                                       CF_UB_similarity_shrink)
# Compute the Prediction for Collaborative Filtering User Based
CF_UB_users_prediction_dictionary = CFAlgorithms.CFUserBasedPredictRecommendation(target_users, CF_user_user_similarity_dictionary,
                                                                                  CF_user_items_dictionary, active_items_to_recommend,
                                                                                  CF_UB_prediction_shrink)

# Write the final Result for Collaborative Filtering User Based
#CFAlgorithms.CFWriteResult('TestDataSet/user_based_map.csv', CF_UB_users_prediction_dictionary)

# Compute the Item-Item Similarity for Collaborative Filtering Item Based
CF_item_item_similarity_dictionary = CFAlgorithms.CFItemItemSimilarity(CF_user_items_dictionary, CF_item_users_dictionary,
                                                                       CF_IB_similarity_shrink)

# Compute the Prediction for Collaborative Filtering Item Based
CF_IB_users_prediction_dictionary = CFAlgorithms.CFItemBasedPredictRecommendation(target_users, CF_item_item_similarity_dictionary,
                                                                                  CF_user_items_dictionary, active_items_to_recommend,
                                                                                  CF_IB_prediction_shrink)
# Write the final Result for Collaborative Filtering Item Based
#CFAlgorithms.CFWriteResult("TestDataSet/item_based_Map.csv", CF_IB_users_prediction_dictionary)

# Compute the Prediction for Collaborative Filtering Hybrid Weighted
#CF_HB_users_prediction_dictionary = CFAlgorithms.CFHybridWeightedPredictRecommendation(CF_UB_users_prediction_dictionary,
#                                                                               CF_IB_users_prediction_dictionary, CF_Hybrid_Weight)

# Write the final Result for Collaborative Filtering Hybrid Weighted
#CFAlgorithms.CFWriteResult("TestDataSet/weight_Map.csv", CF_HB_users_prediction_dictionary)

# Compute the Prediction for Collaborative Filtering Hybrid Rank
CF_HB_2_users_prediction_dictionary = CFAlgorithms.CFHybridRankPredictRecommendation(CF_UB_users_prediction_dictionary,
                                                                                     CF_IB_users_prediction_dictionary, CF_Hybrid_KNN,
                                                                                     CF_User_Rank_Weight, CF_Item_Rank_Weight)

# Write the final Result for Collaborative Filtering Hybrid Rank
CFAlgorithms.CFWriteResult("TestDataSet/rank_Map.csv", CF_HB_2_users_prediction_dictionary)

validation_dictionary = {}
result_dictionary = {}
validation = pd.read_csv('TestDataSet/validationSet.csv', sep=',', header=0)
result = pd.read_csv("TestDataSet/rank_Map.csv", sep=',', header=0)

print ("Create dictionaries for validation and result")
for user, items in validation.values:
    if user in target_users['user_id'].values:
        validation_dictionary[user] = items.split()

for user, items in result.values:
    if (pd.isnull(items)):
        result_dictionary[user] = []
    else:
        item = str(items)
        result_dictionary[user] = item.split()

map = 0
av_prec = 0
for user in validation_dictionary:
    if not result_dictionary.has_key(user):
        continue
    av_prec += va.apk(validation_dictionary[user], result_dictionary[user], 5)

map_at = av_prec / len(validation_dictionary)
map_at = round(map_at,5)
print map_at * 100000