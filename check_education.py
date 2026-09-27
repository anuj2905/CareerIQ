import pandas as pd

df = pd.read_csv(
    "data/resumes/resume_data_for_ranking.csv"
)

print("\nDegree names:")
print(df["degree_names"].head(10).to_list())

print("\nMajor fields:")
print(df["major_field_of_studies"].head(10).to_list())

print("\nJob education requirements:")
print(df["educationaL_requirements"].head(10).to_list())