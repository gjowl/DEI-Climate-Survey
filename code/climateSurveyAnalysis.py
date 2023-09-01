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

  # plot female vs male graphs
  plotFemaleVsMale(df_female, df_male, df_answers, group_compare_question, output_list, output_dir)