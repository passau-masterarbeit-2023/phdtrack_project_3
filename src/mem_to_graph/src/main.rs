use std::path::PathBuf;

// link modules
mod params;
mod tests;
mod graph_data;
mod graph_structs;
mod utils;
mod graph_annotate;
mod graph_embedding;
mod exe_pipeline;

fn main() {
    crate::params::init();

    // call pipeline
    let mut input_path: Vec<std::path::PathBuf> = Vec::new();
    if params::ARGV.file.is_some() {
        let files = params::ARGV.file.as_ref().unwrap();
        for (_, file) in files.iter().enumerate() {
            input_path.push(PathBuf::from(file));
        }
    } else if params::ARGV.directory.is_some() {
        for path in params::ARGV.directory.as_ref().unwrap() {
            input_path.push(PathBuf::from(path));
        }
    } else {
        // default
        input_path.push(params::TESTING_DATA_DIR_PATH.clone());
    }

    // test all provided paths
    for path in input_path.clone() {
        if !path.exists() {
            panic!("🚩 The path doesn't exist: {}", path.to_str().unwrap());
        }
    }

    // launch computations
    for path in input_path {
        crate::exe_pipeline::run(path);
    }
    
}