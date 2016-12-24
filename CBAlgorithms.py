from __future__ import division
import math
import numpy
import operator
from collections import OrderedDict

#Function to initialize users_attributes and attributes_users dictionaries
def InitializeDictionaries_user(user_profile, user_cols):
    # Create the dictionary needed to compute the similarity between users
    # It is the User content matrix build with dictionaries
    # Dictionary is a list of elements, each element is defined as following
    # dict {user -> (list of {attribute -> value})}
    print ("Create users_attributes dictionary")
    users_attributes = {}
    # for each row of the user_profile csv
    for i, row in user_profile.iterrows():
        # initialize the dictionary of the user
        users_attributes[row['user']] = {}
        # for each attribute of the user
        for att in user_cols:
            if not (att == 'user'):
                # if the attribute is job_roles then split the string obtaining the various jobs and insert them in the dictionary
                # if the value of the field job_roles is 0 insert nothing
                if (att == 'job'):
                    if not (row[att] == '0'):
                        jobs = str(row[att]).split(",")
                        for j in jobs:
                            users_attributes[row['user']][att + '_' + str(j)] = 1
                # if the attribute is one of the following consider them only if they are not equal to 0
                elif (att == 'career' or att == 'exp_years' or att == 'exp_years_current'):
                    if not (row[att] == 0 or math.isnan(row[att])):
                        users_attributes[row['user']][att + '_' + str(row[att])] = 1
                # if the attribute is edu_field_of_studies then split the string obtaining the various fields and insert them in
                # the dictionary
                elif (att == 'edu_fiel'):
                    if type(row[att]) == str:
                        fields = str(row[att]).split(",")
                        for f in fields:
                            users_attributes[row['user']][att + '_' + str(f)] = 1
                # if the attribute is country don't consider float values
                elif (att == 'country'):
                    continue
                    #if type(row[att]) == str:
                    #    users_attributes[row['user']][att + '_' + str(row[att])] = 1
                # only the user user having country equal to de has this attribute
                elif (att == 'region'):
                    continue
                    #if (row['country'] == 'de'):
                    #    users_attributes[row['user']][att + '_' + str(row[att])] = 1
                # if the attribute is edu_deg don't consider null value or 0
                elif (att == 'edu_deg'):
                    if not (math.isnan(row[att]) or row[att] == 0):
                        users_attributes[row['user']][att + '_' + str(row[att])] = 1
                # if the column type is int or float discard Null values
                elif (user_profile[att].dtype == numpy.int64 or user_profile[att].dtype == numpy.float64):
                    if not (math.isnan(row[att])):
                        users_attributes[row['user']][att + '_' + str(row[att])] = 1
                else:
                    users_attributes[row['user']][att + '_' + str(row[att])] = 1

    # Create the dictionary containing for each attribute the list of users which have it
    # Dictionary is a list of elements, each element is defined as following
    # dict {attribute -> (list of {user -> value})}
    print ("Create attributes_users dictionary")
    attributes_users = {}
    # for each row of the user_profile csv
    for i, row in user_profile.iterrows():
        # for each attribute of the user
        for att in user_cols:
            if not (att == 'user'):
                # if the attribute is job_roles then split the string obtaining the various jobs and insert them in the dictionary
                # if the value of the field job_roles is 0 insert nothing
                if (att == 'job'):
                    if not (row[att] == '0'):
                        jobs = str(row[att]).split(",")
                        for j in jobs:
                            # if the dictionary is not already initialized do it
                            if not attributes_users.has_key(att + '_' + str(j)):
                                attributes_users[att + '_' + str(j)] = {}
                            attributes_users[att + '_' + str(j)][row['user']] = 1
                # if the attribute is edu_field_of_studies then split the string obtaining the various fields and insert them in
                # the dictionary
                elif (att == 'edu_fiel'):
                    if type(row[att]) == str:
                        fields = str(row[att]).split(",")
                        for f in fields:
                            if not attributes_users.has_key(att + '_' + str(f)):
                                attributes_users[att + '_' + str(f)] = {}
                            attributes_users[att + '_' + str(f)][row['user']] = 1
                # if the attribute is country don't consider float values
                elif (att == 'country'):
                    continue
                    #if type(row[att]) == str:
                    #    if not attributes_users.has_key(att + '_' + str(row[att])):
                    #        attributes_users[att + '_' + str(row[att])] = {}
                    #    attributes_users[att + '_' + str(row[att])][row['user']] = 1
                # only the user user having country equal to de has this attribute
                elif (att == 'region'):
                    continue
                    #if (row['country'] == 'de'):
                    #    if not attributes_users.has_key(att + '_' + str(row[att])):
                    #        attributes_users[att + '_' + str(row[att])] = {}
                    #    attributes_users[att + '_' + str(row[att])][row['user']] = 1
                # if the attribute is one of the following consider them only if they are not equal to 0
                elif (att == 'career' or att == 'exp_years' or att == 'exp_years_current'):
                    if not (row[att] == 0 or math.isnan(row[att])):
                        if not attributes_users.has_key(att + '_' + str(row[att])):
                            attributes_users[att + '_' + str(row[att])] = {}
                        attributes_users[att + '_' + str(row[att])][row['user']] = 1
                # if the attribute is edu_deg don't consider null value or 0
                elif (att == 'edu_deg'):
                    if not (math.isnan(row[att]) or row[att] == 0):
                        if not attributes_users.has_key(att + '_' + str(row[att])):
                            attributes_users[att + '_' + str(row[att])] = {}
                        attributes_users[att + '_' + str(row[att])][row['user']] = 1
                # if the column type is int or float discard Null values
                elif (user_profile[att].dtype == numpy.int64 or user_profile[att].dtype == numpy.float64):
                    if not (math.isnan(row[att])):
                        if not attributes_users.has_key(att + '_' + str(row[att])):
                            attributes_users[att + '_' + str(row[att])] = {}
                        attributes_users[att + '_' + str(row[att])][row['user']] = 1
                else:
                    if not attributes_users.has_key(att + '_' + str(row[att])):
                        attributes_users[att + '_' + str(row[att])] = {}
                    attributes_users[att + '_' + str(row[att])][row['user']] = 1

    return users_attributes, attributes_users

#Function to initialize users_attributes and attributes_users dictionaries
def InitializeDictionaries_item(item_profile, item_cols):
    # Create the dictionary needed to compute the similarity between items
    # It is the item content matrix build with dictionaries
    # Dictionary is a list of elements, each element is defined as following
    # dict {item -> (list of {attribute -> value})}
    print ("Create items_attributes dictionary")
    items_attributes = {}
    # for each row of the item_profile csv
    for i, row in item_profile.iterrows():
        # initialize the dictionary of the user
        items_attributes[row['item']] = {}
        # for each attribute of the item
        for att in item_cols:
            if not (att == 'item'):
                # if the attribute is title or tag then split the string obtaining the various jobs and insert them in the dictionary
                # if the value of the attribute is 0 insert nothing
                if (att == 'title' or att == 'tags'):
                    if not (row[att] == '0'):
                        titles = str(row[att]).split(",")
                        for t in titles:
                            items_attributes[row['item']][att + '_' + str(t)] = 1
                # if the attribute is one of the following consider them only if they are not equal to 0
                elif (att == 'career' or att == 'employ'):
                    if not (row[att] == 0):
                        items_attributes[row['item']][att + '_' + str(row[att])] = 1
                # if the attribute is country don't consider float values
                elif (att == 'country'):
                    continue
                    #if type(row[att]) == str:
                    #    items_attributes[row['item']][att + '_' + str(row[att])] = 1
                # only the item having country equal to de has this attribute
                elif (att == 'region'):
                    continue
                    #if (row['country'] == 'de'):
                    #    items_attributes[row['item']][att + '_' + str(row[att])] = 1
                elif (att == 'created_at' or att == 'active_during_test'):
                    continue
                elif(att == 'latitude' or att == 'longitude'):
                    continue
                # if the column type is int or float discard Null values
                elif (item_profile[att].dtype == numpy.int64 or item_profile[att].dtype == numpy.float64):
                    if not (math.isnan(row[att])):
                        items_attributes[row['item']][att + '_' + str(row[att])] = 1

    # Create the dictionary containing for each attribute the list of users which have it
    # Dictionary is a list of elements, each element is defined as following
    # dict {attribute -> (list of {user -> value})}
    print ("Create attributes_items dictionary")
    attributes_items = {}
    # for each row of the user_profile csv
    for i, row in item_profile.iterrows():
        # for each attribute of the user
        for att in item_cols:
            if not (att == 'item'):
                # if the attribute is title or tag then split the string obtaining the various jobs and insert them in the dictionary
                # if the value of the attribute is 0 insert nothing
                if (att == 'title' or att == 'tags'):
                    if not (row[att] == '0'):
                        titles = str(row[att]).split(",")
                        for t in titles:
                            # if the dictionary is not already initialized do it
                            if not attributes_items.has_key(att + '_' + str(t)):
                                attributes_items[att + '_' + str(t)] = {}
                            attributes_items[att + '_' + str(t)][row['item']] = 1
                # if the attribute is one of the following consider them only if they are not equal to 0
                elif (att == 'career' or att == 'employ'):
                    if not (row[att] == 0):
                        if not attributes_items.has_key(att + '_' + str(row[att])):
                            attributes_items[att + '_' + str(row[att])] = {}
                        attributes_items[att + '_' + str(row[att])][row['item']] = 1
                # if the attribute is country don't consider float values
                elif (att == 'country'):
                    continue
                    #if type(row[att]) == str:
                    #    if not attributes_items.has_key(att + '_' + str(row[att])):
                    #        attributes_items[att + '_' + str(row[att])] = {}
                    #    attributes_items[att + '_' + str(row[att])][row['item']] = 1
                # only the user user having country equal to de has this attribute
                elif (att == 'region'):
                    continue
                    #if (row['country'] == 'de'):
                    #    if not attributes_items.has_key(att + '_' + str(row[att])):
                    #        attributes_items[att + '_' + str(row[att])] = {}
                    #    attributes_items[att + '_' + str(row[att])][row['item']] = 1
                elif (att == 'created_at' or att == 'active_during_test'):
                    continue
                elif(att == 'latitude' or att == 'longitude'):
                    continue
                # if the column type is int or float discard Null values
                elif (item_profile[att].dtype == numpy.int64 or item_profile[att].dtype == numpy.float64):
                    if not (math.isnan(row[att])):
                        if not attributes_items.has_key(att + '_' + str(row[att])):
                            attributes_items[att + '_' + str(row[att])] = {}
                        attributes_items[att + '_' + str(row[att])][row['item']] = 1
    return items_attributes, attributes_items

# Function to compute TF and IDF
def ComputeTF_IDF(users_attributes, attributes_users):
    # create the tf(time frequency) dictionary for each user
    # each attribute of the same user has the same tf value
    users_tf = {}
    for user in users_attributes:#.keys():
        users_tf[user] = 1 / len(users_attributes[user])
    # create the idf dictionary for each attribute
    attributes_idf = {}
    n_users = len(users_attributes.keys())
    for attribute in attributes_users:#.keys():
        attributes_idf[attribute] = math.log10(n_users / len(attributes_users[attribute]))
    # modify each attribute value including tf-idf
    for user in users_attributes:#.keys():
        for attribute in users_attributes[user]:#.keys():
            users_attributes[user][attribute] *= users_tf[user] * attributes_idf[attribute]
            attributes_users[attribute][user] *= users_tf[user] * attributes_idf[attribute]
    # sort the dictionary by attribute values
    for attribute in attributes_users:#.keys():
        attributes_users[attribute] = OrderedDict(
            sorted(attributes_users[attribute].items(), key=lambda t: -t[1]))
    for user in users_attributes:
        users_attributes[user] = OrderedDict(
            sorted(users_attributes[user].items(), key=lambda t: -t[1]))

    return users_attributes, attributes_users

# Function to build the User-User Similarity Dictionary
def CBUserUserSimilarity(target_users_dictionary, user_attributes_dictionary, attributes_users_dictionary, similarity_shrink, KNN):
    # Create the dictionary for the user_user similarity
    # dict {user -> (list of {user -> similarity})}
    user_user_similarity_dictionary = {}
    user_user_similarity_dictionary_num = {}
    user_similarity_dictionary_norm = {}

    print ("Create dictionaries for CB user-user similarity")
    # For each user in the dictionary
    i = 1
    size = len(target_users_dictionary)
    for user in target_users_dictionary:
        print (str(i) + "/" + str(size))
        i = i + 1
        # Calculate the similarity only for the target users
        user_att = user_attributes_dictionary[user] #dictionary of all the attributes of the user
        user_user_similarity_dictionary_num[user] = {}
        # For each attribute of the user
        for att in user_att:
            user_list = attributes_users_dictionary[att].keys() #list of users that has this attribute
            # for first 10 users
            for u in user_list[:550]:
                # Don't consider the similarity between the same users
                if u == user:
                    continue
                else:
                    # Create the dictionary containing the numerator of the similarity
                    if(user_user_similarity_dictionary_num[user].has_key(u)):
                        user_user_similarity_dictionary_num[user][u] += user_attributes_dictionary[user][att] *\
                                                                            user_attributes_dictionary[u][att]
                    else:
                        user_user_similarity_dictionary_num[user][u] = user_attributes_dictionary[user][att] *\
                                                                            user_attributes_dictionary[u][att]
    # For each user in the dictionary
    for user in user_attributes_dictionary:
        # For each attribute of the user
        for attribute in user_attributes_dictionary[user]:
            # Calculate the norm of the vector corresponding to the user attributes
            if (user_similarity_dictionary_norm.has_key(user)):
                user_similarity_dictionary_norm[user] += math.pow(user_attributes_dictionary[user][attribute], 2)
            else:
                user_similarity_dictionary_norm[user] = math.pow(user_attributes_dictionary[user][attribute], 2)
        user_similarity_dictionary_norm[user] = math.sqrt(user_similarity_dictionary_norm[user])

    print ("Similarities estimate:")
    # For each user in the dictionary
    for user in user_user_similarity_dictionary_num:
        user_user_similarity_dictionary[user] = {}
        # Calculate the user-user similarity
        for user_j in user_user_similarity_dictionary_num[user]:
            user_user_similarity_dictionary[user][user_j] = user_user_similarity_dictionary_num[user][user_j] / \
                                                            (user_similarity_dictionary_norm[user] *
                                                             user_similarity_dictionary_norm[user_j] + similarity_shrink)

    if (KNN == 0):
        return user_user_similarity_dictionary
    else:
        user_user_KNN_similarity_dictionary = {}
        for user in user_user_similarity_dictionary:
            user_user_KNN_similarity_dictionary[user] = {}
            KNN_sim_users = sorted(user_user_similarity_dictionary[user].items(), key=operator.itemgetter(1))
            KNN_sim_users_desc = sorted(KNN_sim_users, key=lambda tup: -tup[1])
            for sim_user in KNN_sim_users_desc:
                if (len(user_user_KNN_similarity_dictionary[user]) < KNN):
                    user_user_KNN_similarity_dictionary[user][sim_user[0]] = user_user_similarity_dictionary[user][sim_user[0]]
        return user_user_KNN_similarity_dictionary

# Function to build the Item-Item Similarity Dictionary
def CBItemItemSimilarity(active_items_dictionary, item_attribute_dictionary, attribute_items_dictionary):
    item_item_similarity_dictionary_num = {}
    item_similarity_dictionary_norm = {}

    print ("Create dictionaries for CB item-item similarity")

    i = 1
    size = len(active_items_dictionary)
    for item in active_items_dictionary:
        print (str(i) + "/" + str(size))
        i = i + 1
        item_att = item_attribute_dictionary[item]
        item_item_similarity_dictionary_num[item] = {}
        for att in item_att:
            item_list = attribute_items_dictionary[att].keys()
            for ij in item_list[:100]:
                if ij == item:
                    continue
                else:
                    if(item_item_similarity_dictionary_num[item].has_key(ij)):
                        item_item_similarity_dictionary_num[item][ij] += item_attribute_dictionary[item][att] *\
                                                                         item_attribute_dictionary[ij][att]
                    else:
                        item_item_similarity_dictionary_num[item][ij] = item_attribute_dictionary[item][att] *\
                                                                        item_attribute_dictionary[ij][att]
    for item in item_attribute_dictionary:
        for attribute in item_attribute_dictionary[item]:
            if (item_similarity_dictionary_norm.has_key(item)):
                item_similarity_dictionary_norm[item] += math.pow(item_attribute_dictionary[item][attribute], 2)
            else:
                item_similarity_dictionary_norm[item] = math.pow(item_attribute_dictionary[item][attribute], 2)
        item_similarity_dictionary_norm[item] = math.sqrt(item_similarity_dictionary_norm[item])

    return item_item_similarity_dictionary_num, item_similarity_dictionary_norm

def CBItemItemSimilarityEstimate(item_item_similarity_dictionary, item_similarity_dictionary_norm, similarity_shrink, KNN):
    #item_item_similarity_dictionary = {}
    print ("Similarities estimate:")
    i = 1
    #size = len(item_item_similarity_dictionary_num)
    size = len(item_item_similarity_dictionary)
    #for item in item_item_similarity_dictionary_num:
    for item in item_item_similarity_dictionary:
        print (str(i) + "/" + str(size))
        i = i + 1
        #item_item_similarity_dictionary[item] = {}
        #for item_j in item_item_similarity_dictionary_num[item]:
        for item_j in item_item_similarity_dictionary[item]:
            item_item_similarity_dictionary[item][item_j] = item_item_similarity_dictionary[item][item_j] / \
                                                            (item_similarity_dictionary_norm[item] *
                                                             item_similarity_dictionary_norm[item_j] + similarity_shrink)
                                                            #item_item_similarity_dictionary_num[item][item_j] / \
    if (KNN == 0):
        return item_item_similarity_dictionary
    else:
        #item_item_KNN_similarity_dictionary = {}
        for item in item_item_similarity_dictionary:
            item_item_similarity_dictionary[item] = OrderedDict(sorted(item_item_similarity_dictionary[item].items(), key=lambda t: -t[1]))
            while (len(item_item_similarity_dictionary[item]) > KNN):
                item_to_remove = item_item_similarity_dictionary[item].keys()[-1]
                del item_item_similarity_dictionary[item][item_to_remove]

        return item_item_similarity_dictionary
            #item_item_KNN_similarity_dictionary[item] = {}
            #KNN_sim_items = sorted(item_item_similarity_dictionary[item].items(), key=operator.itemgetter(1))
            #KNN_sim_items_desc = sorted(KNN_sim_items, key=lambda tup: -tup[1])
            #while (len(KNN_sim_items_desc) > KNN):
                #del KNN_sim_items_desc[-1]
            #for sim_item in KNN_sim_items_desc:
                #if (len(item_item_KNN_similarity_dictionary[item]) < KNN):
                    #item_item_KNN_similarity_dictionary[item][sim_item[0]] = item_item_similarity_dictionary[item][sim_item[0]]
        #return item_item_KNN_similarity_dictionary

# Function to create the recommendations for User_Based
def CBUserBasedPredictRecommendation(target_users_dictionary, user_user_similarity_dictionary, user_items_dictionary, active_items_to_recommend,
                                     prediction_shrink):
    print ("Create dictionaries for CB User Based user predictions")
    # Create the dictionary for users prediction
    # dict {user -> (list of {item -> prediction})}
    users_prediction_dictionary = {}
    users_prediction_dictionary_num = {}
    users_prediction_dictionary_norm = {}
    # For each target user
    for user in target_users_dictionary:
        users_prediction_dictionary_num[user] = {}
        # Get dictionary of similar users and the value of similarity
        uus_list = user_user_similarity_dictionary[user]
        # For each similar user in the dictionary
        for user2 in uus_list:
            if(user_items_dictionary.has_key(user2)):
                # Get the dictionary of items with which this user has interact
                u2_item_list = user_items_dictionary[user2]
                #if (user in user_user_similarity_dictionary[user2]):
                    # For each item in the dictionary
                for i in u2_item_list:
                    # If the item was not predicted yet for the user, add it
                    if not (users_prediction_dictionary_num[user].has_key(i)):
                        users_prediction_dictionary_num[user][i] = uus_list[user2] * u2_item_list[i]
                    # Else Evaluate its contribution
                    else:
                        users_prediction_dictionary_num[user][i] += uus_list[user2] * u2_item_list[i]

    # For each user in the dictionary
    for user in user_user_similarity_dictionary:
        users_prediction_dictionary_norm[user] = 0
        # Get the dictionary pointed by the user, containing the similar users
        sim_users = user_user_similarity_dictionary[user]
        for other_user in sim_users:
            users_prediction_dictionary_norm[user] += sim_users[other_user]

    print ("Ratings estimate:")
    # For each target user (users_prediction_dictionary_num contains all target users)
    for user in users_prediction_dictionary_num:
        users_prediction_dictionary[user] = {}
        # For each item predicted for the user
        for item in users_prediction_dictionary_num[user]:
            # Evaluate the prediction of that item for that user
            if (user_items_dictionary.has_key(user)):
                if not (item in user_items_dictionary[user]):
                    if (active_items_to_recommend.has_key(item)):
                        users_prediction_dictionary[user][item] = users_prediction_dictionary_num[user][item] / \
                                                                (users_prediction_dictionary_norm[user] + prediction_shrink)
            else:
                if (active_items_to_recommend.has_key(item)):
                    users_prediction_dictionary[user][item] = users_prediction_dictionary_num[user][item] / \
                                                              (users_prediction_dictionary_norm[user] + prediction_shrink)

    return users_prediction_dictionary

# Function to create the normalized recommendations for User_Based
def CBUserBasedPredictNormalizedRecommendation(target_users_dictionary, user_user_similarity_dictionary, user_items_dictionary, active_items_to_recommend,
                                               prediction_shrink):
    print ("Create dictionaries for CB User Based user predictions")
    # Create the dictionary for users prediction
    # dict {user -> (list of {item -> prediction})}
    users_prediction_dictionary = {}
    users_prediction_dictionary_num = {}
    users_prediction_dictionary_norm = {}
    # For each target user
    for user in target_users_dictionary:
        users_prediction_dictionary_num[user] = {}
        # Get dictionary of similar users and the value of similarity
        uus_list = user_user_similarity_dictionary[user]
        # For each similar user in the dictionary
        for user2 in uus_list:
            if (user_items_dictionary.has_key(user2)):
                # Get the dictionary of items with which this user has interact
                u2_item_list = user_items_dictionary[user2]
                # if (user in user_user_similarity_dictionary[user2]):
                # For each item in the dictionary
                for i in u2_item_list:
                    # If the item was not predicted yet for the user, add it
                    if not (users_prediction_dictionary_num[user].has_key(i)):
                        users_prediction_dictionary_num[user][i] = uus_list[user2] * u2_item_list[i]
                    # Else Evaluate its contribution
                    else:
                        users_prediction_dictionary_num[user][i] += uus_list[user2] * u2_item_list[i]

    # For each user in the dictionary
    for user in user_user_similarity_dictionary:
        users_prediction_dictionary_norm[user] = 0
        # Get the dictionary pointed by the user, containing the similar users
        sim_users = user_user_similarity_dictionary[user]
        for other_user in sim_users:
            users_prediction_dictionary_norm[user] += sim_users[other_user]

    print ("Ratings estimate and Normalization:")
    # For each target user (users_prediction_dictionary_num contains all target users)
    for user in users_prediction_dictionary_num:
        users_prediction_dictionary[user] = {}
        max_prediction = 0
        # For each item predicted for the user
        for item in users_prediction_dictionary_num[user]:
            # Evaluate the prediction of that item for that user
            if (user_items_dictionary.has_key(user)):
                if not (item in user_items_dictionary[user]):
                    if (active_items_to_recommend.has_key(item)):
                        users_prediction_dictionary[user][item] = users_prediction_dictionary_num[user][item] / \
                                                                  (users_prediction_dictionary_norm[user] + prediction_shrink)
                        max_prediction = max(max_prediction, users_prediction_dictionary[user][item])
            else:
                if (active_items_to_recommend.has_key(item)):
                    users_prediction_dictionary[user][item] = users_prediction_dictionary_num[user][item] / \
                                                              (users_prediction_dictionary_norm[user] + prediction_shrink)
                    max_prediction = max(max_prediction, users_prediction_dictionary[user][item])

        for item in users_prediction_dictionary[user]:
            users_prediction_dictionary[user][item] = users_prediction_dictionary[user][item] / max_prediction

    return users_prediction_dictionary

# Function to create the recommendations for Item_Based
def CBItemBasedPredictRecommendation(active_items_dictionary, item_item_similarity_dictionary, user_items_dictionary, target_users_dictionary,
                                     prediction_shrink):
    print ("Create dictionaries for CF Item Based user predictions")
    # Create the dictionary for users prediction
    # dict {user -> (list of {item -> prediction})}
    #users_prediction_dictionary = {}
    users_prediction_dictionary_num = {}
    users_prediction_dictionary_den = {}
    # For each target user
    for uu in target_users_dictionary:
        users_prediction_dictionary_num[uu] = {}
        users_prediction_dictionary_den[uu] = {}
        # If user has interact with at least one item
        if (user_items_dictionary.has_key(uu)):
            # Get dictionary of items with which the user has interact
            i_r_dict = user_items_dictionary[uu]
            # For each item in this dictionary
            for ij in i_r_dict:
                # Get the dictionary of similar items and the value of similarity
                if (ij in active_items_dictionary):
                    ij_s_dict = item_item_similarity_dictionary[ij]
                    # For each similar item in the dictionary
                    for ii in ij_s_dict:
                        if (i_r_dict.has_key(ii)):
                            continue
                        # If the item was not predicted yet for the user, add it
                        if not (users_prediction_dictionary_num[uu].has_key(ii)):
                            users_prediction_dictionary_num[uu][ii] = i_r_dict[ij] * ij_s_dict[ii]
                            users_prediction_dictionary_den[uu][ii] = ij_s_dict[ii]
                        # Else Evaluate its contribution
                        else:
                            users_prediction_dictionary_num[uu][ii] += i_r_dict[ij] * ij_s_dict[ii]
                            users_prediction_dictionary_den[uu][ii] += ij_s_dict[ii]

    print ("Ratings estimate:")
    # For each target user (users_prediction_dictionary_num contains all target users)
    for uu in users_prediction_dictionary_num:
        #users_prediction_dictionary[uu] = {}
        # For each item predicted for the user
        for ii in users_prediction_dictionary_num[uu]:
            # Evaluate the prediction of that item for that user
            if (active_items_dictionary.has_key(ii)):
                users_prediction_dictionary_num[uu][ii] = users_prediction_dictionary_num[uu][ii] / \
                                                      (users_prediction_dictionary_den[uu][ii] + prediction_shrink)

    return users_prediction_dictionary_num

# Function to write the final result of recommendation
def CBWriteResult(output_filename, users_prediction_dictionary):
    sum = 0
    print ("Writing result on " + output_filename)
    out_file = open(output_filename, "w")
    out_file.write('user_id,recommended_items\n')
    for user in users_prediction_dictionary:
        if len(users_prediction_dictionary[user].keys()) > 0:
            users_prediction_dictionary[user] = OrderedDict(
                sorted(users_prediction_dictionary[user].items(), key=lambda t: -t[1]))
        x = users_prediction_dictionary[user].keys()
        x = map(str, x)
        out_file.write(str(user) + ',' + ' '.join(x[:min(len(x), 5)]) + '\n')
        sum += min(len(x), 5)
    left = 50000 - sum
    print(str(left) + " item(s) left in the result")
    out_file.close()