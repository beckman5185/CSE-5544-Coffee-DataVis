#Audrey Beckman
import pandas as pd
from pathlib import Path

def ageFunction(preferenceData, coffeeSurvey):

    #get things with non-null age and preference response
    ageOverall = coffeeSurvey[coffeeSurvey['prefer_overall'].notnull()]['age']
    ageOverall = ageOverall[ageOverall.notnull()]

    #distribution of ages among survey responses
    print(coffeeSurvey['age'].value_counts(normalize=True))

    #unnormalized will show that all preference data have valid age
    overallAge = preferenceData['age'].value_counts(normalize=True)
    print(overallAge)


    #get preference proportions by age group
    ageGroups = preferenceData.groupby('age')['prefer_overall'].value_counts(normalize=True)


    # Notes: coffee D beat by Coffee A/B in >65 and Coffee B/C in 55-64
    return ageGroups.reset_index()


def genderFunction(preferenceData):

    #fewer with not null gender than with normal preference data
    print(len(preferenceData[preferenceData['gender'].notnull()]))


    #looking at distribution of gender in data
    genderOverall = preferenceData['gender'].value_counts(normalize=True)
    #Notes: much more men than women

    #looking at distribution of preference among gender groups
    genderGroups = preferenceData.groupby('gender')['prefer_overall'].value_counts(normalize=True)

    #Notes: women prefer B and C - D and A at bottom of coffee groups
    #Notes: men prefer D and A

    print(genderOverall)
    print(genderGroups)


def educationFunction(preferenceData):
    #fewer with not null education than with normal preference data
    print(len(preferenceData[preferenceData['education_level'].notnull()]))

    #looking at distribution of education in survey responses
    edOverall = preferenceData['education_level'].value_counts(normalize=True)

    #looking at distribution of preferences by education level
    edGroups = preferenceData.groupby('education_level')['prefer_overall'].value_counts(normalize=True)

    #is there correlation between gender and education level?
    #Note: no
    edGender = preferenceData.groupby('education_level')['gender'].value_counts(normalize=True)


    print(edOverall)
    print(edGroups)
    print(edGender)

    #Notes: high school graduate prefer C and D
    #Notes: some college prefer D and B

def raceFunction(preferenceData):


    #fewer with not null race than with normal preference data
    print(len(preferenceData[preferenceData['ethnicity_race'].notnull()]))

    #distribution of race in survey responses
    #Note: relative to US - white and asian groups overrepresented, black and hispanic groups underrepresented
    raceOverall = preferenceData['ethnicity_race'].value_counts(normalize=True)

    #distribution of preference by race
    raceGroups = preferenceData.groupby('ethnicity_race')['prefer_overall'].value_counts(normalize=True)

    #Note: Black people prefer C and D, Hispanic people prefer D and B, Native people prefer C and A

    print(raceOverall)
    print(raceGroups)


def employFunction(preferenceData):
    # fewer with not null employment than with normal preference data
    print(len(preferenceData[preferenceData['employment_status'].notnull()]))

    #distribution of employment in responses
    employOverall = preferenceData['employment_status'].value_counts(normalize=True)

    #distribution of preference by employment
    employGroups = preferenceData.groupby('employment_status')['prefer_overall'].value_counts(normalize=True)

    # Note: retirees prefer B and C, part time prefer D and C


    print(employOverall)
    print(employGroups)


def childFunction(preferenceData):
    # fewer with not null child response than with normal preference data
    print(len(preferenceData[preferenceData['number_children'].notnull()]))

    # distribution of child count in data
    childOverall = preferenceData['number_children'].value_counts(normalize=True)

    #distribution of preferences by child count
    childGroups = preferenceData.groupby('number_children')['prefer_overall'].value_counts(normalize=True)

    # Note: one child - D and C, 3 children - A and D, more than three - B and A

    #does child count correlate with gender?
    #Note: no
    childGender = preferenceData.groupby('number_children')['gender'].value_counts(normalize=True)

    print(childOverall)
    print(childGroups)
    print(childGender)




def polFunction(preferenceData):
    # fewer with not null political alignment than with normal preference data
    print(len(preferenceData[preferenceData['political_affiliation'].notnull()]))

    # distribution of political alignments in data
    polOverall = preferenceData['political_affiliation'].value_counts(normalize=True)

    #distribution of preferences by political alignment
    polGroups = preferenceData.groupby('political_affiliation')['prefer_overall'].value_counts(normalize=True)

    #Note: republicans like D and B, all other almost identical

    #is political affiliation linked with age?
    #Note: yes, 45-64 less likely to be democrats
    polAge = preferenceData.groupby('age')['political_affiliation'].value_counts(normalize=True)

    print(polOverall)
    print(polGroups)
    print(polAge)



def main():

    #get data
    coffeeSurvey= pd.read_csv(Path(__file__).parent/"coffee_survey.csv")

    #read in things with non-null preference data
    preferenceData = coffeeSurvey[coffeeSurvey['prefer_overall'].notnull()]

    #overall distribution of preference among all survey participants
    overallPreference = coffeeSurvey[:]['prefer_overall']
    overallPreference = overallPreference[overallPreference.notnull()]
    overallPreference = preferenceData['prefer_overall'].value_counts(normalize=True)

    print(overallPreference)

    #Note: most people prefer coffee D


    #get normalized age counts
    ageGroups = ageFunction(preferenceData, coffeeSurvey)

    #playing with dataframe
    overallPreference = pd.DataFrame(overallPreference)
    overallPreference['age'] = 'total'
    ageGroups = pd.concat([ageGroups, overallPreference.reset_index()])
    print(overallPreference.reset_index())
    print(ageGroups)


    genderFunction(preferenceData)

    educationFunction(preferenceData)

    raceFunction(preferenceData)

    employFunction(preferenceData)

    childFunction(preferenceData)

    polFunction(preferenceData)


if __name__ == "__main__":
    main()