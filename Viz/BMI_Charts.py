
import seaborn as sns
import pandas as pd
tips = pd.read_csv(r"P:\Coursera\BMI\20161207_testWrite3_mostRecent_trim_grouped.csv")

#di = {1.: "Africa", 2.: "Asia",3.:"Carribbean",4.:"Europe",5.:"Middle East",
#      6.: "Central America",7.:"North America",8.:"Oceania",9.:"South America"}
#
#tips.replace({"Continent": di})

flatui = ["#F781D8","#3498db","#95a5a6"]
sns.set_palette(flatui)
sns.set_context("notebook", font_scale=1, rc={"lines.linewidth": 2})
plt.figure(figsize=(6, 4))
ax = sns.pointplot(y="Continent", x="MeanBMI_BothSexes",hue="Sex", data=tips, join=False, legend=False, hue_order=['Female','Male','Mixed'])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))


#changing the size of the first data series 
points = ax.collections[0]
size = points.get_sizes().item()
new_sizes = [size * .01]
points.set_sizes(new_sizes)

#changing the size of the third data series
points2 = ax.collections[1]
size2 = points2.get_sizes().item()
new_sizes2 = [size2 * .01 ]
points2.set_sizes(new_sizes2)

#changing the size of the third data series
points0 = ax.collections[2]
size0 = points0.get_sizes().item()
new_sizes0= [size0 * 1.5 ]
points0.set_sizes(new_sizes0)

ax.set(xlabel='Mean BMI', ylabel='Continent')

