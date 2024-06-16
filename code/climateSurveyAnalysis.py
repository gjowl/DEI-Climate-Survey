#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   climateSurveyAnalysis.py
@Time    :   2023/05/05 19:48:51
@Author  :   Gilbert Loiseau 
@Version :   1.0
@Contact :   loiseau@wisc.edu
@License :   (C)Copyright 2023, Gilbert Loiseau
@Desc    :   Version of hbarplot for the IPiB survey based on John Ahn's code

Usage: python3 climateSurveyAnalysis.py <data_file> <answer_file>

This script takes in a csv file with the survey data and a csv file with the questions and answers, and
outputs a bar plot for each question with the answers on the y axis and the count on the x axis.
The bar plots are saved in a directory called Questions within the current working directory. 

Notes:
    - The answer file was made by hand and is not automatically generated. It is a csv file from the 
      IPiB_DEI_Climate_Survey_2023_-_For_Distribution_Instrument file, and I had to pay attention to
      the order of the questions (sometimes the 1s and 5s were in flipped orders despite the answers being the same).
    - Some of the questions for dividing the data into groups are hardcoded, so if the question numbers change, be sure
      to change the code as well.
    - Feel free to change the color pallettes to your liking. These are found at the top of the functions.py file.
    - This saves the data into the given output directory (hardcoded below) with individual questions as separate files in that
      directory, and the comparison graphs as separate directories within the output directory.
'''


import sys, os, pandas as pd, numpy as np, matplotlib.pyplot as plt

# define global color palettes
# bar graph color palette
default_color = 'teal'
group_comparison_color = 'navajowhite'
other_color = 'crimson'

# Functions
# get the counts for each answer for a given question
def countAnswers(df, q, answers):
    # initialize the answer counts output
    answer_counts = None
    # check if the question contains a '_'
    if '_' in q:
        # get any columns that match the question
        df_question = df.filter(regex=q)
        # get the counted data for the question
        answer_counts = df_question.apply(pd.Series.value_counts).iloc[0]
        # change the index to the numbered part of the input question
        answer_counts.index = answer_counts.index.str.split('_').str[1]
    else:
        # get the data for the question from the data file
        df_question = df[q]
        # get the column values
        answer_counts = df_question.value_counts()
    return answer_counts

# make a dataframe with the answers and counts for a given question, replacing index with the respective answer
def getAnswerCountDf(answer_counts, answers):
    # sort the answer counts by the index
    answer_counts = answer_counts.sort_index()
    # convert the answer count index to a list
    unique_values = answer_counts.index.tolist()
    # check the length of the unique values list; if 0, then there are no answers for the question
    if len(unique_values) == 0:
        # return an empty dataframe
        return pd.DataFrame({'answer': [], 'count': []})
    # get the smallest value in the unique values list; for some reason the survey center defined some answers with higher numbers than others, so this combats that
    smallest_value = int(min(unique_values))
    # replace the index of each unique value with its corresponding answer
    for i, value in enumerate(unique_values):
        unique_values[i] = answers[int(value)-smallest_value]
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

# plot the bar graph for any percentage based questions
def plotAverageBarGraph(df, question_number, output_dir):
    plt.title(f'{question_number}', fontsize = 10)
    plt.xlabel("Average Percent")
    plt.barh(df['answer'], df['count'], color = default_color)
    plt.savefig(f'{output_dir}/{question_number}.png', bbox_inches="tight")
    plt.clf()

# plot the percent bar graph for any total count based questions
def plotPercentBarGraph(df, question_number, output_dir):
    s = int(df['count'].sum())
    df['count'] = df['count'].apply(lambda x: x/s*100)
    plt.title(f'{question_number}, n={s}', fontsize = 10)
    plt.xlabel("Percentage")
    plt.barh(df['answer'], df['count'], color = default_color)
    plt.xlim(0,100)
    plt.savefig(f'{output_dir}/{question_number}.png', bbox_inches="tight")
    plt.clf()

# plot the bar graph for any total count based questions
def plotBarGraph(df, question_number, output_dir):
    s = int(df['count'].sum())
    plt.title(f'{question_number}, n={s}', fontsize = 10)
    plt.xlabel("Response count")
    plt.barh(df['answer'], df['count'], color = default_color)
    plt.savefig(f'{output_dir}/{question_number}.png', bbox_inches="tight")
    plt.clf()

# gets the average for each answer for a given question; questions 13 and 14 in this version of the survey
def getAnswerAverage(df):
    # remove any NAN values
    df = df.dropna()
    # get the average for each answer
    averages = df.mean()
    # reset the index starting at 1
    averages = averages.reset_index(drop=True)
    averages.index = averages.index + 1
    return averages

# driver function for the analysis
def analyzeAndPlotGraphs(df_data, df_answers, output_dir):
    # loop through the questions and answers
    for q, a in zip(df_answers['Question'], df_answers['Answer']):
        # separate a (answers column) into a list by the pipe as delimiter
        answers = a.split('|')
        # check if the question is question 13 or 14
        if q == 'Q13_' or q == 'Q14_':
            df_question = df_data.filter(regex=q)
            averages = getAnswerAverage(df_question)
            df_count = getAnswerCountDf(averages, answers)
            # reverse the dataframe so the answers are in the correct order (the answers are in reverse order in the data file compared to the original survey)
            df_count = df_count.iloc[::-1]
            plotAverageBarGraph(df_count, q, output_dir)
        elif q == 'Q39_':
            df_question = df_data.filter(regex=q)
            # hardcoding the list of answers for this question here
            q39_answers = ['Strongly disagree','Disagree','Neither agree nor disagree','Somewhat agree','Strongly agree','I do not know']
            # loop through the columns and get the counts for each answer
            for col in df_question.columns:
                answer_counts = df_question[col].value_counts()
                # get the count of the answers
                df_count = getAnswerCountDf(answer_counts, q39_answers)
                # get the number after the '_' in the column name
                col_num = col.split('_')[1]
                # get the question from the answer file by the column number
                label = f'Q39_{answers[int(col_num)-1]}'
                #plotPercentBarGraph(df_count, label, output_dir)
                plotBarGraph(df_count, label, output_dir)
        else:
            # count the answers for the given question
            answer_counts = countAnswers(df_data, q, answers)
            df_count = getAnswerCountDf(answer_counts, answers)
            # reverse the dataframe so the answers are in the correct order (the answers are in reverse order in the data file compared to the original survey)
            df_count = df_count.iloc[::-1]
            #plotPercentBarGraph(df_count, q, output_dir)
            plotBarGraph(df_count, q, output_dir)

def plotComparisonBarGraph(df_count, df_other_count, question_number, label1, label2, color1, color2, output_dir):
    # plot bar graph vertically of df_count and df_all_count
    # get the sum of the counts for each dataframe
    s = int(df_count['count'].sum())
    s_other = int(df_other_count['count'].sum())
    # make copies of the dataframes before transforming the counts to percentages
    df_1 = df_count.copy()
    df_2 = df_other_count.copy()
    # get the percentage of each answer for each dataframe
    df_1['count'] = df_1['count'].apply(lambda x: x/s*100)
    df_2['count'] = df_2['count'].apply(lambda x: x/s_other*100)
    plt.ylim(0,100)
    plt.xticks(rotation=45)
    plt.title(f'{question_number}, {label1}={s}, {label2}={s_other}', fontsize = 10)
    plt.ylabel("Percent")
    bar_width = 0.4
    plt.bar(df_1['answer'], df_1['count'], color = color1, label=label1, width=-bar_width, align = 'edge')
    plt.bar(df_2['answer'], df_2['count'], color = color2, label=label2, width=bar_width, align = 'edge')
    plt.legend()
    plt.savefig(f'{output_dir}/{label1}_{label2}.png', bbox_inches="tight")
    plt.clf()

# question 39 is so different that it needs a separate function ... 
def plotComparisonBarGraph39(df_count, df_other_count, question_number, label1, label2, color1, color2, answer_order, output_dir):
    # plot bar graph vertically of df_count and df_all_count
    # get the sum of the counts for each dataframe
    s = int(df_count['count'].sum())
    s_other = int(df_other_count['count'].sum())
    # make copies of the dataframes before transforming the counts to percentages
    df_1 = df_count.copy()
    df_2 = df_other_count.copy()
    # get the percentage of each answer for each dataframe
    df_1['count'] = df_1['count'].apply(lambda x: x/s*100)
    df_2['count'] = df_2['count'].apply(lambda x: x/s_other*100)

    # set the index to the answer order (for some reason for a couple categories for question 39 this was not in the correct order, so forcing it here)
    df_1 = df_1.set_index('answer').reindex(answer_order).reset_index() 
    plt.ylim(0,100)
    plt.xticks(rotation=45)
    plt.title(f'{question_number}, {label1}={s}, {label2}={s_other}', fontsize = 10)
    plt.ylabel("Percent")
    bar_width = 0.4
    plt.bar(df_1['answer'], df_1['count'], color = color1, label=label1, width=-bar_width, align = 'edge')
    plt.bar(df_2['answer'], df_2['count'], color = color2, label=label2, width=bar_width, align = 'edge')
    plt.legend()
    plt.savefig(f'{output_dir}/{label1}_{label2}.png', bbox_inches="tight")
    plt.clf()

# driver function for the comparison analysis
def analyzeAndPlotComparisonGraphs(df_allData, df_list, df_answers, question_list, output_list, output_dir):
    # loop through the questions and answers
    for df_data, output in zip(df_list, output_list):
        for q, a in zip(df_answers['Question'], df_answers['Answer']):
            # separate a (answers column) into a list by the pipe as delimiter
            answers = a.split('|')
            if q in question_list:
                # get the rest of the data that is not in df_data
                rest_of_data = pd.concat([df_allData, df_data]).drop_duplicates(keep=False)
                # define the output directory and make it if it doesn't exist
                out_dir = f'{output_dir}/{q}'
                os.makedirs(out_dir, exist_ok=True)
                # count the answers for the given question
                all_data_counts = countAnswers(df_allData, q, answers)
                answer_counts = countAnswers(df_data, q, answers)
                rest_counts = countAnswers(rest_of_data, q, answers)
                # get the dataframes for the counts
                df_count = getAnswerCountDf(answer_counts, answers)
                df_all_count = getAnswerCountDf(all_data_counts, answers)
                df_rest_count = getAnswerCountDf(rest_counts, answers)
                # plot the bar graphs
                plotComparisonBarGraph(df_count, df_all_count, q, output, 'All', group_comparison_color, default_color, out_dir)
                plotComparisonBarGraph(df_count, df_rest_count, q, output, 'Rest', group_comparison_color, other_color, out_dir)
            elif q == 'Q39_':
                # kind of a gross way for how I was able to write this for question 39s many groupings
                df_question = df_data.filter(regex=q)
                df_question_all = df_allData.filter(regex=q)
                df_question_rest = rest_of_data.filter(regex=q)
                # hardcoding the list of answers for this question here
                q39_answers = ['Strongly disagree','Disagree','Neutral','Somewhat agree','Strongly agree','I do not know']
                # loop through the columns and get the counts for each answer
                for col in df_question.columns:
                    # count the answers for the given question
                    all_data_counts = df_question_all[col].value_counts() 
                    answer_counts = df_question[col].value_counts()
                    rest_counts = df_question_rest[col].value_counts()
                    # get the dataframes for the counts
                    df_count = getAnswerCountDf(answer_counts, q39_answers)
                    df_all_count = getAnswerCountDf(all_data_counts, q39_answers)
                    df_rest_count = getAnswerCountDf(rest_counts, q39_answers)
                    # get the number after the '_' in the column name
                    col_num = col.split('_')[1]
                    # get the question from the answer file by the column number
                    question_label = f'{answers[int(col_num)-1]}'
                    label = f'Q39_{question_label}'
                    # define the output directory and make it if it doesn't exist
                    out_dir = f'{output_dir}/{label}'
                    os.makedirs(out_dir, exist_ok=True)
                    # plot the bar graphs
                    plotComparisonBarGraph39(df_count, df_all_count, question_label, output, 'All', group_comparison_color, default_color, q39_answers, out_dir)
                    plotComparisonBarGraph39(df_count, df_rest_count, question_label, output, 'Rest', group_comparison_color, other_color, q39_answers, out_dir)
                    

if __name__ == '__main__':
    # read in the command line options
    data_file = sys.argv[1] # input data file
    answer_file = sys.argv[2] # answer file (the one in here is self created; in the future, ask for the file of the answers for each question in this format)

import sys, os, pandas as pd, numpy as np, matplotlib.pyplot as plt
from functions import *

if __name__ == '__main__':
  # read in the command line options
  data_file = sys.argv[1]
  answer_file = sys.argv[2]
  
  # define the output directory and make it if it doesn't exist
  #output_dir = 'Questions'
  output_dir = 'Questions_Percent'
  os.makedirs(output_dir, exist_ok=True)
  
  # read in the data file as a pandas dataframe with all columns as integers
  df_data = pd.read_csv(data_file, sep=',', header=0)
  # remove any columns that contain 'TEXT'; this code only analyzes the multiple choice questions
  df_data = df_data.loc[:, ~df_data.columns.str.contains('TEXT')]
  # read in the answer file as a pandas dataframe
  df_answers = pd.read_csv(answer_file, sep=',', header=0)
  
  # analyze and plot the graphs for each individual question of the data
  #analyzeAndPlotGraphs(df_data, df_answers, output_dir, percent=True)
  
  # define the separated groups of answers (hardcoded); if question numbers change in future surveys, will need to change these
  df_students = df_data[df_data['Q93'] == 1]
  
  # convert the Q58 column to integers and rid of NaN values
  df_data['Q58'] = df_data['Q58'].fillna(0)
  df_data['Q58'] = df_data['Q58'].astype(int)
  
  # keep only the rows that have a value of 5, 6, 7, 8, or 9 in the Q58 column
  df_staff = df_data[df_data['Q58'].isin([6,7,9])]
  df_faculty = df_data[df_data['Q58'].isin([5])]
  
  # divide data into groups based on the following questions
  df_marginalized = df_data[df_data['Q62'] == 1]
  df_lgbtq = df_data[df_data['Q61'] == 1]
  df_first_gen = df_data[df_data['Q63'] == 1]
  df_international = df_data[df_data['Q64'] == 1]
  df_male = df_data[df_data['Q60'] == 'Male']
  df_female = df_data[df_data['Q60'] == 'Female']
  
  # create a list of the dataframes to loop through
  df_list = [df_students, df_staff, df_faculty, df_marginalized, df_lgbtq, df_first_gen, df_international, df_male, df_female]
  
  # create a list of the output directories to loop through
  output_list = ['Students', 'Staff', 'Faculty', 'Marginalized', 'LGBTQ+', 'First Generation College', 'International', 'Male', 'Female'] 
  group_compare_question = ['Q4', 'Q5', 'Q8', 'Q9', 'Q10', 'Q11', 'Q20.0', 'Q21', 'Q30', 'Q56', 'Q39']
  
  # analyze and plot the graphs for comparison between above groups
  #analyzeAndPlotComparisonGraphs(df_data, df_list, df_answers, group_compare_question, output_list, output_dir)
  
  # get the data not found within df_students
  rest_of_data = df_data[~df_data.isin(df_students)].dropna()
>>>>>>> 89763c67d1ca04df31e1e44f42b5d58a82b001aa

  # plot female vs male graphs
  plotFemaleVsMale(df_female, df_male, df_answers, group_compare_question, output_list, output_dir)