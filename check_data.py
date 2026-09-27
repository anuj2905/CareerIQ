# import pandas as pd

# df = pd.read_csv("data/resumes/resume_data_for_ranking.csv")

# # print(df.head())
# # print(df.shape)
# # print(df.columns)
# # print(df.info())
# # print(df.columns.tolist())

# print(df["matched_score"])


import pandas as pd

df = pd.read_csv("data/resumes/resume_data_for_ranking.csv")

# print("\nPositions:")
# print(df["positions"].head(10).to_list())

# print("\nResponsibilities:")
# print(df["responsibilities"].head(10).to_list())

# print("\nJob positions:")
# print(df["job_position_name"].head(10).to_list())

# print("\nJob responsibilities:")
# print(df["responsibilities.1"].head(10).to_list())

print(df.columns)