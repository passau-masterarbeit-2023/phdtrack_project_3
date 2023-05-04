import numpy as np

def load_samples_and_labels_from_csv(csv_file_path: str):
    # Load the data from the CSV file
    data = np.genfromtxt(csv_file_path, delimiter=',', skip_header=1)

    # Extract the labels from the last column
    labels = data[:, -1]

    # Extract the samples from the other columns
    samples = data[:, :-1]

    # Print the shapes of the arrays
    print(f'Shape of labels: {labels.shape}')
    print(f'Shape of samples: {samples.shape}')
