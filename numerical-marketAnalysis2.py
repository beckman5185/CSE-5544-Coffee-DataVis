#Audrey Beckman
import pandas as pd
import statistics

def main():
    coffeeSurvey = pd.read_csv("coffee_survey.csv")

    personal_preference = ['coffee_a_personal_preference','coffee_b_personal_preference',
                           'coffee_c_personal_preference', 'coffee_d_personal_preference']
    bitterness = ['coffee_a_bitterness', 'coffee_b_bitterness', 'coffee_c_bitterness', 'coffee_d_bitterness']

    acidity = ['coffee_a_acidity', 'coffee_b_acidity', 'coffee_c_acidity', 'coffee_d_acidity']

    traitList = personal_preference + bitterness + acidity

    preferenceData = coffeeSurvey[coffeeSurvey[traitList].notnull().all(axis=1)]

    print(preferenceData[traitList])

    #for i in preferenceData[traitList]:
    #    print(preferenceData[i])

    for i in range(len(personal_preference)):

        personalChoice = preferenceData[personal_preference[i]].value_counts(normalize=True)
        print(personalChoice)
        personalMedian = statistics.median(preferenceData[personal_preference[i]])
        print(personalMedian)


    #coffee a is fairly popular, coffee b is ok, coffee c is somewhat popular, coffee d is very popular

    for i in range(len(acidity)):

        acidityChoice = preferenceData[acidity[i]].value_counts(normalize=True)
        print(acidityChoice)
        acidityMedian = statistics.median(preferenceData[acidity[i]])
        print(acidityMedian)

    #coffee A is somewhat acidic, coffees b and c are less acidic, coffee d is fairly acidic

    for i in range(len(bitterness)):

        bitternessChoice = preferenceData[bitterness[i]].value_counts(normalize=True)
        print(bitternessChoice)
        bitternessMedian = statistics.median(preferenceData[bitterness[i]])
        print(bitternessMedian)

    #coffee A and D are not very bitter, coffee b and c are somewhat bitter





if __name__ == "__main__":
    main()