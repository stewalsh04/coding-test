from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import os

summary_file = os.getcwd() + "/" + os.sys.argv[1]

df_break = pd.read_csv(summary_file, sep=",")

#print(df_break)
for col in df_break:
    print(col)
# k means
kmeans = KMeans(n_clusters=2, random_state=0)
df_break['cluster'] = kmeans.fit_predict(df_break[['NormalisedBreaks', 'TotalNormalisedAsiSIbreaks']])
# get centroids
centroids = kmeans.cluster_centers_
cen_x = [i[0] for i in centroids] 
cen_y = [i[1] for i in centroids]
## add to df
df_break['cen_x'] = df_break.cluster.map({0:cen_x[0], 1:cen_x[1]})
df_break['cen_y'] = df_break.cluster.map({0:cen_y[0], 1:cen_y[1]})
# define and map colors
colors = ['#DF2020', '#81DF20']
df_break['c'] = df_break.cluster.map({0:colors[0], 1:colors[1]})

import matplotlib.pyplot as plt
plt.scatter(df_break.NormalisedBreaks, df_break.TotalNormalisedAsiSIbreaks, c=df_break.c, alpha = 0.6, s=10)
plt.title("Summary Plot")
plt.xlabel("Sample")
plt.ylabel("Normalised Count")

output_file = (os.path.join((os.getcwd()), "summary.png"))
plt.savefig(output_file)
