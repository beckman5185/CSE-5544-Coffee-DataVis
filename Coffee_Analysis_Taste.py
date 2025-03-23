import pandas as pd

df = pd.read_csv('coffee_survey.csv')

fav_cols = ['submission_id', 'favorite']
except_fav_cols = [col for col in df.columns if col not in fav_cols]
fav = df.drop(columns=except_fav_cols)
fav = fav.groupby('favorite').count()
fav = fav.reset_index()
fav = fav.rename(columns={'submission_id':'count'})
print(fav)


add_cols = ['submission_id', 'additions']
except_add_cols = [col for col in df.columns if col not in add_cols]
add = df.drop(columns=except_add_cols)
add = add.groupby('additions').count()
print(add)

style_cols = ['submission_id', 'style']
except_style_cols = [col for col in df.columns if col not in style_cols]
style = df.drop(columns=except_style_cols)
style = style.groupby('style').count()
print(style)

roastL_cols = ['submission_id', 'roast_level']
except_roastL_cols = [col for col in df.columns if col not in roastL_cols]
roastL = df.drop(columns=except_roastL_cols)
roastL = roastL.groupby('roast_level').count()
print(roastL)

caffeine_cols = ['submission_id', 'caffeine']
except_caffeine_cols = [col for col in df.columns if col not in caffeine_cols]
caffeine = df.drop(columns=except_caffeine_cols)
caffeine = caffeine.groupby('caffeine').count()
print(caffeine)

