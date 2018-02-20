import os
import csv
import pandas as pd

def location_changed(row1, row2):
    return (row1['Longitude'] !=  row2['Longitude'] or row1['Latitude'] != row2['Latitude'] )

input_dir = "/Users/albertchen/Documents/2018_RA_LSGI_Taxi/obike/"
output_dir = "/Users/albertchen/Documents/2018_RA_LSGI_Taxi/obike/od/"
failed = []
progress = 0
for folder  in  os.listdir(input_dir):
    try:
        for file in os.listdir(input_dir + folder + '/singapore/'):
            try:
                sample_1 = pd.read_csv(input_dir + folder + '/singapore/' + file,
                                        names=['Bike_ID', 'Time', 'Longitude', 'Latitude'])
                sample_1['Date'] = (pd.to_datetime(sample_1['Time'], unit='s') + pd.to_timedelta(8, unit='h')).dt.date
                sample_1['Time'] = (pd.to_datetime(sample_1['Time'], unit='s') + pd.to_timedelta(8, unit='h')).dt.time
                sample_1.sort_values(['Bike_ID', 'Date', 'Time'], inplace=True)
                row_iteration = sample_1.iterrows()
                _, previous_row = next(row_iteration)
                with open(output_dir + file.split('_')[1], 'a') as target:
                     writer = csv.writer(target)
                     writer.writerow(['Date', 'Bike_ID', 'O_Time', 'O_Long', 'O_La', 'D_Time', 'D_Long', 'D_La'])
                     for _, row in row_iteration:
                        if row['Bike_ID'] == previous_row['Bike_ID']:
                            if location_changed(previous_row, row):
                                writer.writerow([previous_row['Date'], previous_row['Bike_ID'],
                                                previous_row['Time'], previous_row['Longitude'],
                                                previous_row['Latitude'],
                                                row['Time'], row['Longitude'], row['Latitude']])
                        previous_row = row
                progress += 1
                print('Progress: ' + str(progress))
            except:
                failed.append(file)


    except:
        failed.append(folder)


print('Process completed with the following folder/files failed: ')
print(failed)