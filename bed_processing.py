import pandas as pd
import os

#Collect inputs
sample_name = os.sys.argv[1]
sample_name = sample_name.split(".")[0]
bed_file = "/home/steve/nextflow/data/breaks/" + (os.sys.argv[2])
intersect_file = (os.getcwd()) + "/" + (os.sys.argv[3])

#Convert to pandas dataframes
df_intersect=pd.read_csv(intersect_file, sep="\t")
df_bed=pd.read_csv(bed_file, sep="\t")

#Calculate the metrics
total_breaks=len(df_bed.index)
total_normalised_breaks=total_breaks/1000
total_intersect=sum(df_intersect.iloc[:,3])
percentage_AsiSI = round((total_intersect/(total_breaks))*100,2)
if total_intersect > 1:
    total_normalised_AsiSIbreaks = round(total_intersect/total_normalised_breaks,2)
else:
    total_normalised_AsiSIbreaks = 0

# Output to CSV files
output_file = (os.path.join((os.getcwd()), "{}.summary.csv".format(sample_name)))         
with open(output_file, 'w') as f:
    [f.write('{0},{1},{2},{3},{4},{5}\n'.format(sample_name,total_breaks,total_normalised_breaks,total_intersect,total_normalised_AsiSIbreaks,percentage_AsiSI))]
