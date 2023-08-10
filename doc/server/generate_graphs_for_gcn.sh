# on the server, use `bg` to run the script in the background
PHDTRACK_DIR=$HOME/phdtrack
OUTPUT_DIR=$PHDTRACK_DIR/phdtrack_project_3/src/mem_to_graph/data/graphs_annotated

# create output dir
mkdir -p $OUTPUT_DIR

# run the rust program
cd $PHDTRACK_DIR/phdtrack_project_3/src/mem_to_graph && cargo run -- -p graph -d $PHDTRACK_DIR/phdtrack_data/Performance_Test -d $PHDTRACK_DIR/phdtrack_data/Training -d $PHDTRACK_DIR/phdtrack_data/Validation -o $OUTPUT_DIR
