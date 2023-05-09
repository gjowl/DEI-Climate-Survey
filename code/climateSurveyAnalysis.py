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

TODO: The script also outputs a csv file with
the counts for each answer for each question. The csv file is saved in the directory called Questions.
'''

import sys, os, pandas as pd, numpy as np, matplotlib.pyplot as plt

def getColumnCountUniqueValues(df, col):
    # get the column values
    value_counts = df[col].value_counts()
    # convert the answer count index to a list
    unique_values = value_counts.index.tolist()
    # sort the answer count by the index
    value_counts = value_counts.sort_index()
    return value_counts 

# get the counts for each answer for a given question
def countAnswers(df, q, answers):
    # initialize the answer counts output
    answer_counts = None
    # check if the question contains a '_'
    if '_' in q:
        # get any columns that match the question
        df_question = df.filter(regex=q)
        # get the first row of the answer counts
        answer_counts = df_question.apply(pd.Series.value_counts).iloc[0]
        # get the number of the column after the '_' for the answer_counts
        answer_counts.index = answer_counts.index.str.split('_').str[1]
    else:
        # get the data for the question from the data file
        df_question = df[q]
        # get the column values
        answer_counts = df_question.value_counts()
        # sort the answer count by the index
        answer_counts = answer_counts.sort_index()
    return answer_counts

# make a dataframe with the answers and counts for a given question, replacing index with the respective answer
def getAnswerCountDf(answer_counts, answers):
    # convert the answer count index to a list
    unique_values = answer_counts.index.tolist()
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

def plotAverageBarGraph(df, question_number, output_dir):
    plt.title(f'{question_number}', fontsize = 10)
    plt.xlabel("Average Percent")
    # plot the bar histogram for response vs count
    plt.barh(df['answer'], df['count'], color = 'teal')
    plt.savefig(f'{output_dir}/{question_number}.png', bbox_inches="tight")
    plt.clf()

def plotBarGraph(df, question_number, output_dir):
    s = int(df['count'].sum())
    plt.title(f'{question_number}, n={s}', fontsize = 10)
    plt.xlabel("Response count")
    # plot the bar histogram for response vs count
    plt.barh(df['answer'], df['count'], color = 'teal')
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

if __name__ == '__main__':
    # read in the command line options
    data_file = sys.argv[1]
    answer_file = sys.argv[2]

    # define the output directory and make it if it doesn't exist
    output_dir = 'Questions'
    os.makedirs(output_dir, exist_ok=True)

    # read in the data file as a pandas dataframe with all columns as integers
    df_data = pd.read_csv(data_file, sep=',', header=0)
    # read in the answer file as a pandas dataframe
    df_answers = pd.read_csv(answer_file, sep=',', header=0)

    # loop through the questions and answers
    for q, a in zip(df_answers['Question'], df_answers['Answer']):
        # separate a into a list of answers by the pipe as delimiter
        answers = a.split('|')
        # check if the question is question 13 or 14
        if q == 'Q13_' or q == 'Q14_':
            df_question = df_data.filter(regex=q)
            averages = getAnswerAverage(df_question)
            df_count = getAnswerCountDf(averages, answers)
            plotAverageBarGraph(df_count, q, output_dir)
        elif q == 'Q39_':
            df_question = df_data.filter(regex=q)
            # hardcoding the list of answers for this question here
            q39_answers = ['Strongly disagree','Disagree','Neither agree nor disagree','Somewhat agree','Strongly agree','I do not know']
            print(df_question)
            # loop through the columns and get the counts for each answer
            for col in df_question.columns:
                answer_counts = df_question[col].value_counts()
                # sort the answer counts by the index
                answer_counts = answer_counts.sort_index()
                # get the count of the answers
                df_count = getAnswerCountDf(answer_counts, q39_answers)
                print(df_count)
                # get the number after the '_' in the column name
                col_num = col.split('_')[1]
                # get the question from the answer file by the column number
                label = f'Q39_{answers[int(col_num)-1]}'
                plotBarGraph(df_count, label, output_dir)
        else:
            # count the answers for the given question
            answer_counts = countAnswers(df_data, q, answers)
            df_count = getAnswerCountDf(answer_counts, answers)
            plotBarGraph(df_count, q, output_dir)
    
    # split columns
    split_col = ['Q60', 'Q61']
    # separate the data by the given columns
    #for col in split_col:
    #    split_data = getColumnCountUniqueValues(df_data, col)
    #    # rid of any indices with less than 5 counts
    #    split_data = split_data[split_data > 5]
    #    # keep the data that matches the indices of the split data
    #    df_data = df_data[df_data[col].isin(split_data.index)]
    #    # can from here analyze the data for each individual split
    #    # TODO: add in the analysis part here
