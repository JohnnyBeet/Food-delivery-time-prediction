import os
import glob
from cmdstanpy import CmdStanModel
import pandas as pd

# change cwd to project folder
os.chdir('/home')

# load and prepare data
df = pd.read_csv('new_data_delivery.csv', delimiter=',', decimal='.')
df = df[df["Road distances [km]"] < 30]
train_df = pd.DataFrame(df.iloc[:, :])
train_df["Normalized distances"] = (train_df["Road distances [km]"] - train_df["Road distances [km]"].mean()) / train_df["Road distances [km]"].std()
train_df["Normalized mealprep"] = (train_df["Meal_preparation_time"] - train_df["Meal_preparation_time"].mean()) / train_df["Meal_preparation_time"].std()
road_density_map = {'Jam ':1, 'High ':2, 'Medium ':3, 'Low ':4}
train_df["Road_traffic_density"] = train_df["Road_traffic_density"].apply(lambda x: road_density_map[x])
train_df["Normalized person_rating"] = (train_df["Delivery_person_Ratings"] - train_df["Delivery_person_Ratings"].mean()) / train_df["Delivery_person_Ratings"].std()
train_df["multiple_deliveries"] = (train_df["multiple_deliveries"]+1).astype(int)


# remove previously fitted models (they weight a lot)
files = glob.glob('models_output/model[1-2]/fit/*')
for f in files:
    os.remove(f)


# create and sample from first model
model1_fit=CmdStanModel(stan_file='model1_fit.stan')
model1_sample=model1_fit.sample(data={"N": len(train_df), 
                                    "distance": train_df["Normalized distances"].values,
                                    "meal_preparation_time": train_df["Normalized mealprep"].values, 
                                    "delivery_times": train_df["Time_taken(min)"].values, 
                                    "traffic_level" :train_df["Road_traffic_density"].values},
                     iter_sampling=1000,
                     iter_warmup=1000, 
                     chains=4,
                     output_dir='models_output/model1/fit/'
                         )

# write model diagnostics
temp=model1_sample.diagnose()
with open("models_output/model1/output.txt", "w") as file:
    file.write(temp)

# delete model 1 from memory (it weighs around 4GBs...)
del model1_fit, model1_sample, temp


# create and sample from second model
model2_fit=CmdStanModel(stan_file='model2_fit.stan')
model2_sample=model2_fit.sample(data={"N": len(train_df), 
                                    "distance": train_df["Normalized distances"].values,
                                    "meal_preparation_time": train_df["Normalized mealprep"].values, 
                                    "delivery_times": train_df["Time_taken(min)"].values, 
                                    "traffic_level" :train_df["Road_traffic_density"].values,                           
                                    "delivery_person_rating": train_df["Normalized person_rating"].values,
                                    "number_of_deliveries": train_df["multiple_deliveries"].values}, 
                     iter_sampling=1000,
                     iter_warmup=1000, 
                     chains=4,
                     output_dir='models_output/model2/fit/'
                         )

temp=model2_sample.diagnose()
with open("models_output/model2/output.txt", "w") as file:
    file.write(temp)

# no need to delete, python's gc will take care of that