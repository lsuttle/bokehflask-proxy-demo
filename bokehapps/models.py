import pandas as pd


def make_vector(input_list):

    model_columns = [\
     'teachers',\
     'percent_lunch_aid',\
     'students',\
     'students_per_dollar',\
     'students_reached',\
     'total_price_excluding_optional_support',\
     'has_giving_page_t',\
     'top500_giving_t',\
     'title1_Yes',\
     'launch_month_1',\
     'launch_month_2',\
     'launch_month_3',\
     'launch_month_4',\
     'launch_month_5',\
     'launch_month_6',\
     'launch_month_7',\
     'launch_month_8',\
     'launch_month_9',\
     'launch_month_10',\
     'launch_month_11',\
     'launch_month_12',\
     'school_state_AK',\
     'school_state_AL',\
     'school_state_AR',\
     'school_state_AZ',\
     'school_state_CA',\
     'school_state_CO',\
     'school_state_CT',\
     'school_state_DC',\
     'school_state_DE',\
     'school_state_FL',\
     'school_state_GA',\
     'school_state_HI',\
     'school_state_IA',\
     'school_state_ID',\
     'school_state_IL',\
     'school_state_IN',\
     'school_state_KS',\
     'school_state_KY',\
     'school_state_LA',\
     'school_state_MA',\
     'school_state_MD',\
     'school_state_ME',\
     'school_state_MI',\
     'school_state_MN',\
     'school_state_MO',\
     'school_state_MS',\
     'school_state_MT',\
     'school_state_NC',\
     'school_state_ND',\
     'school_state_NE',\
     'school_state_NH',\
     'school_state_NJ',\
     'school_state_NM',\
     'school_state_NV',\
     'school_state_NY',\
     'school_state_OH',\
     'school_state_OK',\
     'school_state_OR',\
     'school_state_PA',\
     'school_state_RI',\
     'school_state_SC',\
     'school_state_SD',\
     'school_state_TN',\
     'school_state_TX',\
     'school_state_UT',\
     'school_state_VA',\
     'school_state_VT',\
     'school_state_WA',\
     'school_state_WI',\
     'school_state_WV',\
     'school_state_WY',\
     'primary_focus_subject_Applied Sciences',\
     'primary_focus_subject_Character Education',\
     'primary_focus_subject_Civics & Government',\
     'primary_focus_subject_College & Career Prep',\
     'primary_focus_subject_Community Service',\
     'primary_focus_subject_ESL',\
     'primary_focus_subject_Early Development',\
     'primary_focus_subject_Economics',\
     'primary_focus_subject_Environmental Science',\
     'primary_focus_subject_Extracurricular',\
     'primary_focus_subject_Financial Literacy',\
     'primary_focus_subject_Foreign Languages',\
     'primary_focus_subject_Gym & Fitness',\
     'primary_focus_subject_Health & Life Science',\
     'primary_focus_subject_Health & Wellness',\
     'primary_focus_subject_History & Geography',\
     'primary_focus_subject_Literacy',\
     'primary_focus_subject_Literature & Writing',\
     'primary_focus_subject_Mathematics',\
     'primary_focus_subject_Music',\
     'primary_focus_subject_Nutrition',\
     'primary_focus_subject_Other',\
     'primary_focus_subject_Parent Involvement',\
     'primary_focus_subject_Performing Arts',\
     'primary_focus_subject_Social Sciences',\
     'primary_focus_subject_Special Needs',\
     'primary_focus_subject_Team Sports',\
     'primary_focus_subject_Visual Arts',\
     'resource_type_Books',\
     'resource_type_Other',\
     'resource_type_Supplies',\
     'resource_type_Technology',\
     'resource_type_Trips',\
     'resource_type_Visitors',\
     'poverty_level_high poverty',\
     'poverty_level_highest poverty',\
     'poverty_level_low poverty',\
     'poverty_level_moderate poverty',\
     'grade_level_Grades 3-5',\
     'grade_level_Grades 6-8',\
     'grade_level_Grades 9-12',\
     'grade_level_Grades PreK-2',\
     'eligible_double_your_impact_match_t',\
     'eligible_almost_home_match_t']

    feature_vector = pd.DataFrame(index=[0], columns=model_columns)



    feature_vector['has_giving_page_t'] = input_list[0]
    feature_vector['top500_giving_t'] = input_list[1]
    feature_vector['title1_Yes'] = input_list[2]
    feature_vector['eligible_double_your_impact_match_t'] = input_list[3]
    feature_vector['eligible_almost_home_match_t'] = input_list[4]
    feature_vector['teachers'] = input_list[5]
    feature_vector['students'] = input_list[6]
    feature_vector['students_reached'] = input_list[7]
    feature_vector['total_price_excluding_optional_support'] = input_list[8]
    feature_vector['students_per_dollar'] = input_list[7]*1.0/input_list[8]
    feature_vector['percent_lunch_aid'] = input_list[9]

    month_lookup = {\
     'January':'launch_month_1',\
     'February':'launch_month_2',\
     'March':'launch_month_3',\
     'April':'launch_month_4',\
     'May':'launch_month_5',\
     'June':'launch_month_6',\
     'July':'launch_month_7',\
     'August':'launch_month_8',\
     'September':'launch_month_9',\
     'October':'launch_month_10',\
     'November':'launch_month_11',\
     'December':'launch_month_12',\
               }

    month_columns = [\
     'launch_month_1',\
     'launch_month_2',\
     'launch_month_3',\
     'launch_month_4',\
     'launch_month_5',\
     'launch_month_6',\
     'launch_month_7',\
     'launch_month_8',\
     'launch_month_9',\
     'launch_month_10',\
     'launch_month_11',\
     'launch_month_12']

    feature_vector[month_columns] = 0
    feature_vector[month_lookup[input_list[10]]] = 1

    state_columns = [\
     'school_state_AK',\
     'school_state_AL',\
     'school_state_AR',\
     'school_state_AZ',\
     'school_state_CA',\
     'school_state_CO',\
     'school_state_CT',\
     'school_state_DC',\
     'school_state_DE',\
     'school_state_FL',\
     'school_state_GA',\
     'school_state_HI',\
     'school_state_IA',\
     'school_state_ID',\
     'school_state_IL',\
     'school_state_IN',\
     'school_state_KS',\
     'school_state_KY',\
     'school_state_LA',\
     'school_state_MA',\
     'school_state_MD',\
     'school_state_ME',\
     'school_state_MI',\
     'school_state_MN',\
     'school_state_MO',\
     'school_state_MS',\
     'school_state_MT',\
     'school_state_NC',\
     'school_state_ND',\
     'school_state_NE',\
     'school_state_NH',\
     'school_state_NJ',\
     'school_state_NM',\
     'school_state_NV',\
     'school_state_NY',\
     'school_state_OH',\
     'school_state_OK',\
     'school_state_OR',\
     'school_state_PA',\
     'school_state_RI',\
     'school_state_SC',\
     'school_state_SD',\
     'school_state_TN',\
     'school_state_TX',\
     'school_state_UT',\
     'school_state_VA',\
     'school_state_VT',\
     'school_state_WA',\
     'school_state_WI',\
     'school_state_WV',\
     'school_state_WY']
    feature_vector[state_columns] = 0

    if input_list[11] is not 'All':
        state_string = 'school_state_' + str(input_list[11])
        feature_vector[state_string] = 1

    primary_focus_columns =[\
     'primary_focus_subject_Applied Sciences',\
     'primary_focus_subject_Character Education',\
     'primary_focus_subject_Civics & Government',\
     'primary_focus_subject_College & Career Prep',\
     'primary_focus_subject_Community Service',\
     'primary_focus_subject_ESL',\
     'primary_focus_subject_Early Development',\
     'primary_focus_subject_Economics',\
     'primary_focus_subject_Environmental Science',\
     'primary_focus_subject_Extracurricular',\
     'primary_focus_subject_Financial Literacy',\
     'primary_focus_subject_Foreign Languages',\
     'primary_focus_subject_Gym & Fitness',\
     'primary_focus_subject_Health & Life Science',\
     'primary_focus_subject_Health & Wellness',\
     'primary_focus_subject_History & Geography',\
     'primary_focus_subject_Literacy',\
     'primary_focus_subject_Literature & Writing',\
     'primary_focus_subject_Mathematics',\
     'primary_focus_subject_Music',\
     'primary_focus_subject_Nutrition',\
     'primary_focus_subject_Other',\
     'primary_focus_subject_Parent Involvement',\
     'primary_focus_subject_Performing Arts',\
     'primary_focus_subject_Social Sciences',\
     'primary_focus_subject_Special Needs',\
     'primary_focus_subject_Team Sports',\
     'primary_focus_subject_Visual Arts']

    feature_vector[primary_focus_columns] = 0
    if input_list[12] is not 'All':
        subject_string = 'primary_focus_subject_' + str(input_list[12])
        feature_vector[subject_string] = 1

    resource_columns = [\
     'resource_type_Books',\
     'resource_type_Other',\
     'resource_type_Supplies',\
     'resource_type_Technology',\
     'resource_type_Trips',\
     'resource_type_Visitors']

    feature_vector[resource_columns] = 0
    if input_list[13] is not 'All':
        resource_string = 'resource_type_' + str(input_list[13])
        feature_vector[resource_string] = 1

    poverty_columns = [\
     'poverty_level_high poverty',\
     'poverty_level_highest poverty',\
     'poverty_level_low poverty',\
     'poverty_level_moderate poverty']

    feature_vector[poverty_columns] = 0
    if input_list[14] is not 'All':
        poverty_string = 'poverty_level_' + str(input_list[14])
        feature_vector[poverty_string] = 1

    grade_columns = [\
     'grade_level_Grades 3-5',\
     'grade_level_Grades 6-8',\
     'grade_level_Grades 9-12',\
     'grade_level_Grades PreK-2']

    feature_vector[grade_columns] = 0
    if input_list[15] is not 'All':
        grade_string = 'grade_level_' + str(input_list[15])
        feature_vector[grade_string] = 1

    return feature_vector

def make_changes(user_data,model):

    user_data = user_data.iloc[0]
    base_score = model.predict_proba(user_data.values.reshape(1,-1))[:,1]

    flip_giving = user_data.copy()
    change = (user_data['has_giving_page_t']+1)%2
    if change == 1:
        rec = "Joining a giving page "
    else:
        rec = "Not being part of a giving page "
    flip_giving['has_giving_page_t']=change
    new_prob = model.predict_proba(flip_giving.values.reshape(1,-1))[:,1]
    net_change = new_prob-base_score
    if net_change > 0:
        sign_change = 'raise'
    else:
        sign_change = 'lower'
    changes = pd.DataFrame({'change':[rec], 'score':[new_prob], 'net_change':[net_change], 'sign_change':[sign_change]})


    flip_giving_500 = user_data.copy()
    change = (user_data['top500_giving_t']+1)%2
    if change == 1:
        rec = "Joining a giving page with over 100 projects "
    else:
        rec = "Not being part of a giving page with over 100 projects "
    flip_giving_500['top500_giving_t']=change
    new_prob = model.predict_proba(flip_giving_500.values.reshape(1,-1))[:,1]
    net_change = new_prob-base_score
    if net_change > 0:
        sign_change = 'raise'
    else:
        sign_change = 'lower'
    changes = pd.concat([changes,pd.DataFrame({'change':[rec], 'score':[new_prob], 'net_change':[net_change], 'sign_change':[sign_change]},index = [len(changes)])])


    flip_double_impact = user_data.copy()
    change = (user_data['eligible_double_your_impact_match_t']+1)%2
    if change == 1:
        rec = "Framing your project to be eligible for a 'Double Your Impact' matching program "
    else:
        rec = "Not participating in a 'Double Your Impact' matching program "
    flip_double_impact['eligible_double_your_impact_match_t']=change
    new_prob = model.predict_proba(flip_double_impact.values.reshape(1,-1))[:,1]
    net_change = new_prob-base_score
    if net_change > 0:
        sign_change = 'raise'
    else:
        sign_change = 'lower'
    changes = pd.concat([changes,pd.DataFrame({'change':[rec], 'score':[new_prob], 'net_change':[net_change], 'sign_change':[sign_change]},index = [len(changes)])])


    flip_almost_home = user_data.copy()
    change = (user_data['eligible_almost_home_match_t']+1)%2
    if change == 1:
        rec = "Framing your project to be eligible for an 'Almost Home' offer "
    else:
        rec = "Not participating in an 'Almost Home' offer "
    flip_almost_home['eligible_almost_home_match_t']=change
    new_prob = model.predict_proba(flip_almost_home.values.reshape(1,-1))[:,1]
    net_change = new_prob-base_score
    if net_change > 0:
        sign_change = 'raise'
    else:
        sign_change = 'lower'
    changes = pd.concat([changes,pd.DataFrame({'change':[rec], 'score':[new_prob], 'net_change':[net_change], 'sign_change':[sign_change]},index = [len(changes)])])


    price_up_10 = user_data.copy()
    change = user_data['total_price_excluding_optional_support']*1.1
    rec = 'Increasing the amount of funds requested by 10% '
    price_up_10['total_price_excluding_optional_support'] = change
    new_prob = model.predict_proba(price_up_10.values.reshape(1,-1))[:,1]
    net_change = new_prob-base_score
    if net_change > 0:
        sign_change = 'raise'
    else:
        sign_change = 'lower'
    changes = pd.concat([changes,pd.DataFrame({'change':[rec], 'score':[new_prob], 'net_change':[net_change], 'sign_change':[sign_change]},index = [len(changes)])])


    price_down_10 = user_data.copy()
    change = user_data['total_price_excluding_optional_support']*0.9
    rec = 'Decreasing the amount of funds requested by 10% '
    price_down_10['total_price_excluding_optional_support'] = change
    new_prob = model.predict_proba(price_down_10.values.reshape(1,-1))[:,1]
    net_change = new_prob-base_score
    if net_change > 0:
        sign_change = 'raise'
    else:
        sign_change = 'lower'
    changes = pd.concat([changes,pd.DataFrame({'change':[rec], 'score':[new_prob], 'net_change':[net_change], 'sign_change':[sign_change]},index = [len(changes)])])


    month_lookup = {\
                    'launch_month_1':'January',\
                    'launch_month_2':'February',\
                    'launch_month_3':'March',\
                    'launch_month_4':'April',\
                    'launch_month_5':'May',\
                    'launch_month_6':'June',\
                    'launch_month_7':'July',\
                    'launch_month_8':'August',\
                    'launch_month_9':'September',\
                    'launch_month_10':'October',\
                    'launch_month_11':'November',\
                    'launch_month_12':'December',\
                   }

    for month in range(1,13):
        month_changes = user_data.copy()
        month_string = 'launch_month_'+str(month)
        month_set = set(range(1,13))-set([month])
        month_changes[month_string] = 1
        month_changes[month_set] = 0
        rec = 'Launching the project in %s ' % month_lookup[month_string]
        new_prob = model.predict_proba(month_changes.values.reshape(1,-1))[:,1]
    net_change = new_prob-base_score
    if net_change > 0:
        sign_change = 'raise'
    else:
        sign_change = 'lower'
    changes = pd.concat([changes,pd.DataFrame({'change':[rec], 'score':[new_prob], 'net_change':[net_change], 'sign_change':[sign_change]},index = [len(changes)])])

    #changes.sort(['score'], inplace = True, ascending = False)
    changes.sort_values(['score'], inplace = True, ascending = False)
    #print changes

    base_score_sentence = 'Your current score is %.2f%%' % (base_score*100)
    recommendation_dataframe = pd.DataFrame({'Rec_Number':'Baseline Score', 'Recommendation':base_score_sentence, 'Score': base_score*100}, index = [0])

    for row_num in range(3):
        recommendation = changes.iloc[row_num]
        rec_string = "%swill %s your score by %.2f%% to %.2f%%" % (recommendation['change'],recommendation['sign_change'],recommendation['net_change'][0]*100,recommendation['score'][0]*100)
        recommendation_dataframe = pd.concat([recommendation_dataframe,pd.DataFrame({'Rec_Number':'Rec '+str(len(recommendation_dataframe)),'Recommendation':[rec_string],"Score":recommendation['score'][0]*100},index = [len(recommendation_dataframe)])])
    return recommendation_dataframe

    #ecommendation_dataframe = recommendation_dataframe.reset_index()
    #recommendation_dataframe['index'] = recommendation_dataframe.index.astype(str)

    #return recommendation_dataframe
