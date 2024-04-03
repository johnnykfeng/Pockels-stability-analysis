import pandas as pd
import os

# main folder with all the data
root_directory = "Z:\\R&D\\Personal\\Shreya\\Stability"

# initialize empty list of dataframes
dfs = []

# loop over folders in the main folder (Test Folders 1 - 20)
for test_folder in sorted(
    [d for d in os.listdir(root_directory) if d.isdigit()], key=int
):
    # if current path is not a sensor_id_folder, skip to the next loop
    if not os.path.isdir(
        os.path.join(root_directory, test_folder)
    ):
        continue

    # loop ocver all the folders in the test folders
    # (5 different sensors in each folder)
    for sensor_id_folder in sorted(
        os.listdir(os.path.join(root_directory, test_folder))
    ):
        # if current path is not a sensor_id_folder, skip to the next loop
        if not os.path.isdir(
            os.path.join(root_directory, test_folder, sensor_id_folder)
        ):
            continue

        # file naming patterns
        file1 = sensor_id_folder + "_summary.xlsx"
        file2 = sensor_id_folder + "_missing_voltage.xlsx"

        # extract SensorID and test sequence from sensor_id_folder
        sensor_id = sensor_id_folder
        test_sequence = "Test " + test_folder

        # read excel files
        df1 = pd.read_excel(
            os.path.join(root_directory, test_folder,
                         sensor_id_folder, file1),
            engine="openpyxl",
        )
        df2 = pd.read_excel(
            os.path.join(root_directory, test_folder,
                         sensor_id_folder, file2),
            engine="openpyxl",
        )

        # remove first two columns from the second DataFrame
        df2 = df2.iloc[:, 2:]
        df = pd.concat([df1, df2], axis=1)

        # add SensorID and test sequence columns before data
        df.insert(0, "SensorID", sensor_id)
        df.insert(1, "TestSequence", test_sequence)

        # add each indiviudal sensor test data to list of dataframes
        dfs.append(df)

    # final data frame that holds the combined data from all sensors and tests
    combined_df = pd.concat(dfs, ignore_index=True)

    # converts the strings from Test Sequence column 
    # to integers so they're ordered properly
    combined_df["TestSequence"] = (
        combined_df["TestSequence"].str.extract("(\d+)").astype(int)
    )

    # sort combined data by SensorID and test sequence
    combined_df.sort_values(by=["SensorID", "TestSequence"], inplace=True)

save_folder = r"./"

# write combined data to new excel file
combined_df.to_excel(
    os.path.join(save_folder, "stability_full_data.xlsx"), 
    index=False
)

combined_df.to_csv(
    os.path.join(save_folder, "stability_full_data.csv"), 
    index=False
)

print("Data has been combined and saved")
print(f"as stability_full_data in {save_folder}")
