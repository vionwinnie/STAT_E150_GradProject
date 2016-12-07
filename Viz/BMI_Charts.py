#Reading the file into Python
import seaborn as sns
import pandas as pd
tips = pd.read_csv(r"P:\Coursera\BMI\20161207_testWrite3_mostRecent_trim_grouped.csv")

#di = {1.: "Africa", 2.: "Asia",3.:"Carribbean",4.:"Europe",5.:"Middle East",
#      6.: "Central America",7.:"North America",8.:"Oceania",9.:"South America"}
#
#tips.replace({"Continent": di})

#setting the color for different series 
flatui = ["#95a5a6",  "#F781D8","#3498db"]
sns.set_palette(flatui)

#setting the size of the plot, size of the font 
sns.set_context("notebook", font_scale=1, rc={"lines.linewidth": 2})
plt.figure(figsize=(6, 4))

ax = sns.pointplot(y="Continent", x="MeanBMI_BothSexes",hue="Sex", data=tips, join=False, legend=False)

#adding the legend to the right side of the plot
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))


#changing the size of the second data series 
points = ax.collections[1]
size = points.get_sizes().item()
new_sizes = [size * .01 if name.get_text() != "Fri" else size for name in ax.get_yticklabels()]
points.set_sizes(new_sizes)

#changing the size of the third data series
points2 = ax.collections[2]
size2 = points2.get_sizes().item()
new_sizes2 = [size2 * .01 if name.get_text() != "Fri" else size for name in ax.get_yticklabels()]
points2.set_sizes(new_sizes2)

#rename axes
ax.set(xlabel='Mean BMI', ylabel='Continent')

