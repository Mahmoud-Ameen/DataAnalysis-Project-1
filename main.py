import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re


data = pd.read_csv("Hobbies and Academic Performance (Responses) - Form Responses 1.csv")

# clean hours columns:
def clean_hours(text):
    if isinstance(text, str):
        numbers = re.findall(r'\d+', text)

        if numbers:
            if '-' in text or ':' in text or 'or' in text:
                # If it's a range, take the average
                # for example : "12-20", "3 or 4"
                nums = [int(num) for num in numbers]
                return np.mean(nums)
            else:
                return int(numbers[0])    
                
    return np.nan

data['Hobbies_Hours'] = data['Hobbies_Hours'].apply(clean_hours)
data['Hobbies_Hours'] = pd.to_numeric(data['Hobbies_Hours'], errors='coerce')


data['Studying_Hours'] = data['Studying_Hours'].apply(clean_hours)
data['Studying_Hours'] = pd.to_numeric(data['Studying_Hours'], errors='coerce')

################
# clean and split Hobbies column

def clean_Hobbies(text):
    # Remove the "(e.g., ...)" part from each category
    text = re.sub(r'\(e\.g\.,.*?\)', '', text)
    
    categories = [category.split('(')[0].strip() for category in text.split(',')]
    categories = [category.replace('Socializing/Spending time with friends', 'Socializing') for category in categories]
    return categories

data['Hobbies'] = data['Hobbies'].apply(clean_Hobbies)

########################################################
print(data.describe())


def scatterPlots():
    global data

    # Scatter plot between GPA and hours spent on hobbies
    plt.figure(figsize=(8, 6))
    plt.scatter(data['Hobbies_Hours'], data['GPA'], color='blue', alpha=0.7,s=100)
    plt.title('Scatter Plot: GPA vs Hours Spent on Hobbies')
    plt.xlabel('Hours Spent on Hobbies')
    plt.ylabel('GPA')
    plt.grid(True)
    plt.show()

    # Scatter plot between hours spent on hobbies and hours spent studying
    plt.figure(figsize=(8, 6))
    plt.scatter(data['Hobbies_Hours'], data['Studying_Hours'], color='green', alpha=0.7,s=100)
    plt.title('Scatter Plot: Hours Spent on Hobbies vs Hours Spent Studying')
    plt.xlabel('Hours Spent on Hobbies')
    plt.ylabel('Hours Spent Studying')
    plt.grid(True)
    plt.show()

    # Graph showing the relation between the type of hobby and GPA
    data = data.explode('Hobbies')

    plt.figure(figsize=(10, 6))
    hobby_gpa = data.groupby('Hobbies')['GPA'].mean().sort_values()
    hobby_gpa.plot(kind='bar', color='orange')
    plt.title('Relation Between Hobbies and average GPA of students engaging in this hobby')
    plt.xlabel('Hobby')
    plt.ylabel('Average GPA')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y')
    plt.show()

def boxPlots():
    plt.boxplot(data['Hobbies_Hours'],vert=False,meanline=True,showmeans=True,showfliers=True)
    plt.xlabel("Hours spent engaging in hobbies")
    plt.show()

    plt.boxplot(data['Studying_Hours'],vert=False,meanline=True,showmeans=True,showfliers=True)
    plt.xlabel("Hours spent Studying")
    plt.show()

    plt.boxplot(data['GPA'],vert=False,meanline=True,showmeans=True,showfliers=True)
    plt.xlabel("GPA")
    plt.show()


scatterPlots()
boxPlots()