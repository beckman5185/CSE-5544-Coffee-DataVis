#Audrey Beckman
import pandas as pd
import matplotlib.pyplot as plt

def ageFunction(preferenceData, coffeeSurvey):

    #ageOverall = coffeeSurvey[coffeeSurvey['prefer_overall'].notnull()]['age']
    #ageOverall = ageOverall[ageOverall.notnull()]

    #age distribution including null values for preference
    #print(coffeeSurvey['age'].value_counts(normalize=True))

    #unnormalized will show that all preference data have valid age
    overallAge = preferenceData['age'].value_counts(normalize=True)

    print(overallAge)

    #preferA = preferenceData[preferenceData['prefer_overall']=='Coffee A']
    #preferB = preferenceData[preferenceData['prefer_overall']=='Coffee B']
    #preferC = preferenceData[preferenceData['prefer_overall'] == 'Coffee C']
    #preferD = preferenceData[preferenceData['prefer_overall'] == 'Coffee D']

    #ageA = preferA['age'].value_counts(normalize=False)
    #ageB = preferB['age'].value_counts(normalize=False)
    #ageC = preferC['age'].value_counts(normalize=False)
    #ageD = preferD['age'].value_counts(normalize=False)

    #print(ageA)
    #print(ageB)
    #print(ageC)
    #print(ageD)

    ageGroups = preferenceData.groupby('age')['prefer_overall'].value_counts(normalize=True)

    print(ageGroups)

    # coffee D beat by Coffee A/B in >65 and Coffee B/C in 55-64


def genderFunction(preferenceData):


    #fewer with not null gender than with normal preference data
    print(len(preferenceData[preferenceData['gender'].notnull()]))

    #much more men than women

    genderOverall = preferenceData['gender'].value_counts(normalize=True)
    genderGroups = preferenceData.groupby('gender')['prefer_overall'].value_counts(normalize=True)

    #women prefer B and C - D and A at bottom of coffee groups
    #men prefer D and A

    print(genderOverall)
    print(genderGroups)


def educationFunction(preferenceData):
    # fewer with not null gender than with normal preference data
    print(len(preferenceData[preferenceData['education_level'].notnull()]))

    edOverall = preferenceData['education_level'].value_counts(normalize=True)
    edGroups = preferenceData.groupby('education_level')['prefer_overall'].value_counts(normalize=True)

    #edGender = preferenceData.groupby('education_level')['gender'].value_counts(normalize=True)


    print(edOverall)
    print(edGroups)
    #print(edGender)

    #high school graduate prefer C and D
    #some college prefer D and B

def raceFunction(preferenceData):


    #fewer with not null gender than with normal preference data
    print(len(preferenceData[preferenceData['ethnicity_race'].notnull()]))

    #relative to US - white and asian groups overrepresented, black and hispanic groups underrepresented



    raceOverall = preferenceData['ethnicity_race'].value_counts(normalize=True)
    raceGroups = preferenceData.groupby('ethnicity_race')['prefer_overall'].value_counts(normalize=True)

    #black people prefer C and D, hispanic people prefer D and B, native people prefer C and A

    print(raceOverall)
    print(raceGroups)


def employFunction(preferenceData):
    # fewer with not null gender than with normal preference data
    print(len(preferenceData[preferenceData['employment_status'].notnull()]))

    # relative to US - white and asian groups overrepresented, black and hispanic groups underrepresented

    employOverall = preferenceData['employment_status'].value_counts(normalize=True)
    employGroups = preferenceData.groupby('employment_status')['prefer_overall'].value_counts(normalize=True)

    # retirees prefer B and C, part time prefer D and C


    print(employOverall)
    print(employGroups)


def childFunction(preferenceData):
    # fewer with not null gender than with normal preference data
    print(len(preferenceData[preferenceData['number_children'].notnull()]))

    # relative to US - white and asian groups overrepresented, black and hispanic groups underrepresented

    childOverall = preferenceData['number_children'].value_counts(normalize=True)
    childGroups = preferenceData.groupby('number_children')['prefer_overall'].value_counts(normalize=True)

    # one child - D and C, 3 children - A and D, more than three - B and A

    #childGender = preferenceData.groupby('number_children')['gender'].value_counts(normalize=True)

    print(childOverall)
    print(childGroups)
    #print(childGender)




def polFunction(preferenceData):
    # fewer with not null gender than with normal preference data
    print(len(preferenceData[preferenceData['political_affiliation'].notnull()]))

    # relative to US - white and asian groups overrepresented, black and hispanic groups underrepresented

    polOverall = preferenceData['political_affiliation'].value_counts(normalize=True)
    polGroups = preferenceData.groupby('political_affiliation')['prefer_overall'].value_counts(normalize=True)

    # one child - D and C, 3 children - A and D, more than three - B and A

    #republicans like D and B, all other almost identical

    #45-64 less likely to be democrats
    #polAge = preferenceData.groupby('age')['political_affiliation'].value_counts(normalize=True)

    print(polOverall)
    print(polGroups)
    #print(polAge)








def main():

    coffeeSurvey = pd.read_csv("coffee_survey.csv")


    preferenceData = coffeeSurvey[coffeeSurvey['prefer_overall'].notnull()]


    overallPreference = coffeeSurvey[:]['prefer_overall']
    overallPreference = overallPreference[overallPreference.notnull()]

    overallPreference = preferenceData['prefer_overall'].value_counts(normalize=True)

    print(overallPreference)





    #most people prefer coffee D


    #ageFunction(preferenceData, coffeeSurvey)

    #genderFunction(preferenceData)

    #educationFunction(preferenceData)

    #raceFunction(preferenceData)

    #employFunction(preferenceData)

    #childFunction(preferenceData)

    polFunction(preferenceData)


if __name__ == "__main__":
    main()