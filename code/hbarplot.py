#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   hbarplot.py
@Time    :   2023/05/05 19:48:51
@Author  :   Gilbert Loiseau 
@Version :   1.0
@Contact :   loiseau@wisc.edu
@License :   (C)Copyright 2023, Gilbert Loiseau
@Desc    :   Version of hbarplot for the IPiB survey based on John Ahn's code
'''

import sys, os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def getColumnCountUniqueValues(df, col):
    # get the column values
    value_counts = df[col].value_counts()
    # convert the answer count index to a list
    unique_values = value_counts.index.tolist()
    # remove any
    # sort the answer count by the index
    value_counts = value_counts.sort_index()
    return value_counts 

def getAnswerCountDf(answer_counts, answers):
    # convert the answer count index to a list
    unique_values = answer_counts.index.tolist()
    # replace the index of each unique value with its corresponding answer
    for i, value in enumerate(unique_values):
        unique_values[i] = answers[int(value)-1]
    # check if there are any values that are not in the answers
    if len(unique_values) != len(answers):
        # add the missing values to the unique values with a count of 0
        for i in range(len(answers)):
            if answers[i] not in unique_values:
                unique_values.append(answers[i])
                answer_counts = pd.concat([answer_counts, pd.Series([0], index=[i+1])])
    # create a new dataframe with the answers and counts
    output_df = pd.DataFrame({'answer': unique_values, 'count': answer_counts.values})
    return output_df 

# read in the command line options
data_file = sys.argv[1]
answer_file = sys.argv[2]

# read in the data file as a pandas dataframe with all columns as integers
df_data = pd.read_csv(data_file, sep=',', header=0)
df_answers = pd.read_csv(answer_file, sep=',', header=0)

# split columns
split_col = ['Q60', 'Q61']
# separate the data by the given columns
for col in split_col:
    split_data = getColumnCountUniqueValues(df_data, col)
    # rid of any indices with less than 5 counts
    split_data = split_data[split_data > 5]
    # keep the data that matches the indices of the split data
    df_data = df_data[df_data[col].isin(split_data.index)]
    # can from here analyze the data for each individual split
    # TODO: add in the analysis part here

# loop through the answer columns
# loop through the questions and answers
for q, a in zip(df_answers['Question'], df_answers['Answer']):
    # separate a into a list of answers
    answers = a.split('|')
    # loop through the columns in the data file
    for col in df_data.columns:
        # check if the column is the question
        if col == q:
            # get the column values
            answer_counts = df_data[col].value_counts()
            # sort the answer count by the index
            answer_counts = answer_counts.sort_index()
            # setup a dataframe with each answer and its count; this is the answer count per answer for the input question
            df_count = getAnswerCountDf(answer_counts, answers)
            # from here, wok with df_count to plot the data for every question for whatever you want to do
            # next I think I'll take a look at how John Ahn did it, and hopefully just copy paste that in here!
            s = df_count['count'].sum()
            plt.title(f'{q}, n={s}', fontsize = 10)
            plt.xlabel("Response count")
            # plot the bar histogram for response vs count
            plt.barh(df_count['answer'], df_count['count'], color = 'teal')
            plt.savefig(f'{q}.png', bbox_inches="tight")
            exit(0)


    # get the answer from the answer column
    col = 'Q' + str(q) + '_ANSWER'


t1 = ["Extremely committed", "Very committed", "Somewhat committed", "Not at all committed"]
t2 = ["Extremely important", "Very important", "Moderately important", "Slightly important", "Not at all important"]
t3 = ["Extremely often", "Very often", "Sometimes", "Rarely", "Never"]
t4 = ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]
t5 = ["A supervisor", "A colleague or peer", "A non-supervisory faculty member", "Other"]
t6 = ["Yes", "Maybe", "No"]
t7 = ["I have all the information I need about this.", "I have heard about some resources, but do not know how to engage with them.", "I totally lack information about this."]
t8 = ["Yes, very much so", "Yes, somewhat", "Neutral", "No, not really", "No, not at all"]
t9 = ["Race or ethnicity", "Sexual orientation", "Gender identity", "Age", "Disability", "Religion or belief systems", "Political ideology", "Socioeconomic status", "Language or accent", "National origin", "Parental/familial/marital status", "Not related to personal identity", "Unsure", "Other (please explain)"]
t10 = ["Faculty trainer in IPiB", "Faculty outside of IPiB", "Student in IPiB", "Student outside of IPiB", "Staff (Research or administrative)", "Post-doc", "Other (please explain)"]
t11 = ["Yes, more than once", "Yes, once", "No", "Not sure"]
t12 = ["Yes", "No", "I don't know"]
t13 = ["Strongly disagree", "Disagree", "Neither agree nor disagree", "Somewhat agree", "Strongly agree", "I don't know"]
t14 = ["Yes", "No"]
t15 = ["Yes, repeatedly", "Yes, occasionally", "No, not really", "No, never"]
t16 = ["Yes, very much so", "Yes, somewhat", "No, not really", "No, not at all"]
t17 = ["Undergraduate student", "Pre-dissertator", "Dissertator", "Post-doc", "Faculty trainer", "Research staff", "Administrative staff", "Other (please explain)"]
t18 = ["Yes", "No", "Prefer not to say"]
t19 = ["Faculty trainer in IPiB", "Faculty outside of IPiB", "Student in IPiB", "Student outside of IPiB", "Staff (Research or administrative)", "Post-doc", "Other (Please explain)"]
t20 = ["Race or ethnicity", "Sexual orientation", "Gender identity", "Age", "Disability", "Religion or belief systems", "Political ideology", "Socioeconomic status", "Language or accent", "National origin", "Parental/familial/marital status", "Not related to personal identity", "Unsure", "Other, please explain"]

t_t = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20]

def ordAns(df_slice, t_t):
    s = set(df_slice)
    s = [x for x in s if str(x) != 'nan']
    ldf = len(s)
    ret = []
    #print("S is " + str(s))
    for i in t_t:
        #print(i)
        e = []
        for j in i:
            #print("J is " + str(j))
            if j in s:
                e.append(True)
                #print(e)
            else:
                e.append(False)
            #print("E is " + str(e))
        if len(e)>3:
            #print("S is " + str(s))
            if "Neutral" in s:
                if e.count(True) >= 4:
                    ret=i
            elif "Other (Please explain)" in s:
                if e.count(True) == 7:
                    ret = i
            elif "Other (please explain)" in s:
                #print("Identified: Other (please explain)")
                #print("S is " + str(s))
                if e.count(True) >= 7:
                    ret = i
                    #print("This should be the correct ret: ")
                    #print(ret)
                if "Undergraduate student" in s:
                    ret = t_t[16]
                if "Other, please explain" in ret:
                    ret = t_t[8]
                if "Faculty trainer in IPiB" in s:
                    ret = t_t[9]

            elif "Other, please explain" in s:
                if e.count(True) >=7:
                    ret = i
            else:
                if e.count(True) >= 4:
                    ret = i
        if len(e)==3:
            if e.count(True) == 3:
                ret = i
        if len(e)==2:
            if ("Maybe" not in s) and ("I don't know" not in s) and ("Prefer not to say" not in s) and ("Yes, more than once" not in s):
                if e.count(True) >= 1:
                    ret = i
    return ret



def trB(df, label):
    new_df = []
    for i in range(len(df)):
        if df[i] == label:
            new_df.append(df[i])
            
    return new_df


#requires going from 1 to 5
def neOrd(df, new_label_list):
    df_nl = []
    for i in new_label_list:
        df_n = trB(df,i)
        a = df_n.count(i)
        df_nl.append(a)
    s = sum(df_nl)
        
    return df_nl, s

def hBar(df, sli, q_number,t_t):
    d = df.iloc[:,sli]
    nll = ordAns(d,t_t)
    #nll.reverse()
    print(nll)
    d_bp, s = neOrd(d,nll)
    print(d_bp)
    plt.title(q_number +  ", n=" + str(s), fontsize = 10)
    plt.xlabel("Response count")
    plt.barh(nll,d_bp, color = "teal")
    plt.savefig("" + str(q_number) + ".png", bbox_inches="tight")
    plt.show()
    
    
def multCh(df, c1, c2):
    sl = df.iloc[:,c1:c2]
    rows, cols = sl.shape
    comp = []
    for i in range(rows):
        for j in range(cols):
            comp.append(sl.iloc[i,j])
    comp = [x for x in comp if str(x) != 'nan']
    comp = [x for x in comp if str(x) != ' ']
    #print(comp)
    comp = pd.DataFrame(comp)
    return comp

df = pd.read_excel(r"Z:/General/John Ahn/Coyle Lab/IPiB DEI Committee/IPiB Survey/IPiB Survey Data All_Redacted.xlsx", index_col = 0)

'''
hBar(df, 14,"Question 11", t_t)
hBar(df, 62,"Question 26", t_t)
hBar(df, 177,"Question 64", t_t)
hBar(df, 178,"Question 65", t_t)
'''

'''
hBar(df, 7,"Question 4", t_t)
hBar(df, 11,"Question 8", t_t)


hBar(df, 32,"Question 17", t_t)

hBar(df, 61,"Question 25", t_t)


hBar(df, 113,"Question 34", t_t)

hBar(df, 165,"Question 53", t_t)
hBar(df, 168,"Question 56", t_t)


hBar(df, 175,"Question 62", t_t)
'''

#hBar(df, 139,"Question 39 Women", t_t)
hBar(df, 140,"Question 39 LGBQ+", t_t)
#hBar(df, 141,"Question 39 Transgender or Genderqueer", t_t)
hBar(df, 142,"Question 39 Marginalized racial ethnic groups", t_t)
#hBar(df, 143,"Question 39 Individuals of strong religious beliefs", t_t)
hBar(df, 144,"Question 39 Individuals of underrepresented religious groups", t_t)
#hBar(df, 145,"Question 39 Individuals of financially disadvantaged backgrounds", t_t)
hBar(df, 146,"Question 39 Individuals with physical disabilities", t_t)
#hBar(df, 147,"Question 39 Individuals with learning disabilities", t_t)
hBar(df, 148,"Question 39 Individuals with mental illnesses", t_t)
#hBar(df, 149,"Question 39 Individuals with caregiving responsibilities", t_t)
hBar(df, 150,"Question 39 Individuals with conservative political beliefs", t_t)
