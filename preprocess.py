def preprocess_data(data):
    # Drop the first column
    data = data.iloc[:, 1:]
    
    # List of columns to drop
    cols_to_drop = ['Mouse position X', 'Mouse position Y', 'Fixation point X (MCSnorm)', 'Fixation point Y (MCSnorm)',
                    'Event', 'Event value',
                    'Computer timestamp', 'Export date', 'Recording date',
                    'Recording date UTC', 'Recording start time', 'Timeline name', 'Recording Fixation filter name',
                    'Recording software version', 'Recording resolution height', 'Recording resolution width',
                    'Recording monitor latency', 'Presented Media width', 'Presented Media height',
                    'Presented Media position X (DACSpx)', 'Presented Media position Y (DACSpx)', 'Original Media width',
                    'Recording start time UTC', 'Original Media height', 'Sensor']


    # Forward fill the pupil diameter and fixation point columns
    data[['Pupil diameter left', 'Pupil diameter right', 'Fixation point X', 'Fixation point Y']] = \
        data[['Pupil diameter left', 'Pupil diameter right', 'Fixation point X', 'Fixation point Y']].ffill()

    # List of columns to be converted to numerical values
    num_cols = ['Gaze direction left X', 'Gaze direction left Y', 'Gaze direction left Z',
                'Gaze direction right X', 'Gaze direction right Y', 'Gaze direction right Z',
                'Eye position left X (DACSmm)', 'Eye position left Y (DACSmm)', 'Eye position left Z (DACSmm)',
                'Eye position right X (DACSmm)', 'Eye position right Y (DACSmm)', 'Eye position right Z (DACSmm)',
                'Gaze point left X (DACSmm)', 'Gaze point left Y (DACSmm)', 'Gaze point right X (DACSmm)',
                'Gaze point right Y (DACSmm)', 'Gaze point X (MCSnorm)', 'Gaze point Y (MCSnorm)',
                'Gaze point left X (MCSnorm)', 'Gaze point left Y (MCSnorm)', 'Gaze point right X (MCSnorm)',
                'Gaze point right Y (MCSnorm)', 'Pupil diameter left', 'Pupil diameter right']

    # Convert the string values into numbers
    for col in num_cols:
        data[col] = pd.to_numeric(data[col].str.replace(',', '.'), errors='coerce')

   
   
    return data
    
def summarize_eye_tracking_data(data, group):
 
    valid_data = data[(data['Validity left'] == 'Valid') & (data['Validity right'] == 'Valid')]


    total_fixations = data[data['Eye movement type'] == 'Fixation'].shape[0]

    
    avg_fixation_duration = data[data['Eye movement type'] == 'Fixation']['Gaze event duration'].mean()

    # Calculate mean, median, and std of pupil diameter, Gaze point X, Gaze point Y, Fixation point X, and Fixation point Y
    pupil_diameter_stats = data[['Pupil diameter left', 'Pupil diameter right']].mean(axis=1).agg(['mean', 'median', 'std']).rename(lambda x: f'Pupil Diameter {x.capitalize()}')
    gaze_point_x_stats = data['Gaze point X'].agg(['mean', 'median', 'std']).rename(lambda x: f'Gaze Point X {x.capitalize()}')
    gaze_point_y_stats = data['Gaze point Y'].agg(['mean', 'median', 'std']).rename(lambda x: f'Gaze Point Y {x.capitalize()}')
    fixation_point_x_stats = data['Fixation point X'].agg(['mean', 'median', 'std']).rename(lambda x: f'Fixation Point X {x.capitalize()}')
    fixation_point_y_stats = data['Fixation point Y'].agg(['mean', 'median', 'std']).rename(lambda x: f'Fixation Point Y {x.capitalize()}')

    # Create summary row
    summary_data = {
        'Participant Name': data['Participant name'].iloc[0],
        'Project Name': group,
        'Recording Name': data['Recording name'].iloc[0],
        'Total Fixations': total_fixations,
        'Avg. Fixation Duration': avg_fixation_duration
    }
    summary_data.update(pupil_diameter_stats)
    summary_data.update(gaze_point_x_stats)
    summary_data.update(gaze_point_y_stats)
    summary_data.update(fixation_point_x_stats)
    summary_data.update(fixation_point_y_stats)

    summary = pd.DataFrame(summary_data, index=[0])

    return summary