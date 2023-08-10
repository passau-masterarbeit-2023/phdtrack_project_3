PHDTRACK_DATA_DIR=$HOME/phdtrack/phdtrack_data

mkdir -p $PHDTRACK_DATA_DIR

# download original dataset
wget -O $PHDTRACK_DATA_DIR/Performance_Test.zip https://zenodo.org/record/6537904/files/Performance%20Test.zip?download=1
wget -O $PHDTRACK_DATA_DIR/README.md https://zenodo.org/record/6537904/files/README.md?download=1
wget -O $PHDTRACK_DATA_DIR/Training.zip https://zenodo.org/record/6537904/files/Training.zip?download=1
wget -O $PHDTRACK_DATA_DIR/Validation.zip https://zenodo.org/record/6537904/files/Validation.zip?download=1

# unzip original dataset
unzip $PHDTRACK_DATA_DIR/Performance_Test.zip -d $PHDTRACK_DATA_DIR
mv 'Performance Test'/ Performance_Test
unzip $PHDTRACK_DATA_DIR/Training.zip -d $PHDTRACK_DATA_DIR
unzip $PHDTRACK_DATA_DIR/Validation.zip -d $PHDTRACK_DATA_DIR
