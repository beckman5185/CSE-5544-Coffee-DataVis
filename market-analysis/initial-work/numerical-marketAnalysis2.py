#Audrey Beckman
import pandas as pd
import statistics

def main():
    #get data
    coffeeSurvey = pd.read_csv("coffee_survey.csv")

    #get trait lists
    personal_preference = ['coffee_a_personal_preference','coffee_b_personal_preference',
                           'coffee_c_personal_preference', 'coffee_d_personal_preference']
    bitterness = ['coffee_a_bitterness', 'coffee_b_bitterness', 'coffee_c_bitterness', 'coffee_d_bitterness']
    acidity = ['coffee_a_acidity', 'coffee_b_acidity', 'coffee_c_acidity', 'coffee_d_acidity']

    #compile trait lists
    traitList = personal_preference + bitterness + acidity

    #get data not null for traits
    preferenceData = coffeeSurvey[coffeeSurvey[traitList].notnull().all(axis=1)]

    print(preferenceData[traitList])

    #get personal preference per coffee
    for i in range(len(personal_preference)):

        #counts of each rating
        personalChoice = preferenceData[personal_preference[i]].value_counts(normalize=True)
        print(personalChoice)
        #median rating
        personalMedian = statistics.median(preferenceData[personal_preference[i]])
        print(personalMedian)


    #Note: coffee a is fairly popular, coffee b is ok, coffee c is somewhat popular, coffee d is very popular

    #get acidity per coffee
    for i in range(len(acidity)):

        #counts of each rating
        acidityChoice = preferenceData[acidity[i]].value_counts(normalize=True)
        print(acidityChoice)
        #median rating
        acidityMedian = statistics.median(preferenceData[acidity[i]])
        print(acidityMedian)

    #Note: coffee A is somewhat acidic, coffees b and c are less acidic, coffee d is fairly acidic

    #get bitterness per coffee
    for i in range(len(bitterness)):

        #counts of each rating
        bitternessChoice = preferenceData[bitterness[i]].value_counts(normalize=True)
        print(bitternessChoice)
        #median rating
        bitternessMedian = statistics.median(preferenceData[bitterness[i]])
        print(bitternessMedian)

    #Note: coffee A and D are not very bitter, coffee b and c are somewhat bitter





if __name__ == "__main__":
    main()