# Worklog

## Meetings

### Meeting - Fri 17th 2023

These are the next steps for the project

* [ ] A LOT of refactoring. Compress the pointer representation within weight of edges. We are only interested in the relationship between data structures.
* [ ] Feature engineering: find the most significative features and their related hyper-parameters.

  * [ ] allocation size in the DTN
  * [ ] offset in the DTN (position of the value node inside the DTN)
  * [ ] number of PN and VN in DTNs

## Work

### Wed 10 Mai 2023

`python main.py -p univariate_fs -o testing`: launch the feature engineering program.

* [ ] investigate Sklearn data batches
* [ ] Code in rust a verification step to check generated samples and labels files.
* [ ] Find and fix the `nan` value being computer for p-values of feature 5.
* [ ] Complete feature importance sorting.



Investigation: We have a problem with a `Nan` value for column 5, after feature scoring using `SelectKBest(f_classif, k=10)`...

```shell
(array([ 2.13664457e+03,  3.05970593e+03,  2.35275725e+02,  2.89164262e+03,
       -6.27668700e+06,  2.71689523e+03,  2.23123122e+04,  1.61600075e+04,
        1.71411695e+04,  8.67881935e+01,  8.35089205e+01,  5.22530786e+04,
        5.43860569e+04,  1.79539777e+03,  1.79875998e+03,  6.58822038e+01,
        6.53073932e+01,  1.83736984e+04]), array([0.00000000e+00, 0.00000000e+00, 4.22489491e-53, 0.00000000e+00,
                  nan, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 1.20825541e-20, 6.34471438e-20, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 4.78779757e-16,
       6.40917066e-16, 0.00000000e+00]))
```

Trying to look at samples and labels data doen't reveal any NaN or Inf values...

```python
# detect NaN and infinite values  
print(np.isnan(samples).any())  # Check if there are any NaN values in the samples
print(np.isinf(samples).any())  # Check if there are any infinite values in the samples
print(np.isnan(labels).any())  # Check if there are any NaN values in the labels
print(np.isinf(labels).any())  # Check if there are any infinite values in the labels
```

```python
False
False
False
False
```

Trying to determine the range of the 5th column :

```python
 column_index = 4  # (fifth column of index 4) Replace this with the index of the column causing NaN values
    print("Min Max (f_dtns_ancestor_1):", samples[:, column_index].min(), samples[:, column_index].max())  # Print min and max values of the specific column
    print("Any NaN? (f_dtns_ancestor_1):", np.isnan(samples[:, column_index]).any())  # Check if there are any NaN values in the specific column
    print("Any Inf? (f_dtns_ancestor_1):", np.isinf(samples[:, column_index]).any())  # Check if there are any infinite values in the specific column

    # print the set of unique values in the fifth column
    print("Set of unique values (f_dtns_ancestor_1):", np.unique(samples[:, column_index]))
```

```shell
Min Max (f_dtns_ancestor_1): 1 1
Any NaN? (f_dtns_ancestor_1): False
Any Inf? (f_dtns_ancestor_1): False
Set of unique values (f_dtns_ancestor_1): [1]
```

The range is null, so here it is. The 5th column is the first DTN ancestor wich is always 1 because every value node is in a DTN. We must eliminate every unvariant column (wich is meaningless)

### Mon 8 Mai 2023

* [X] Create a pipeline for data loading and checking
* [X] remove data checking from other pipelines
* [X] correct and optimize `check_samples_and_labels`
* [X] correct error `ValueError: Found input variables with inconsistent numbers of samples: [5194279, 6059402]`

We fixed the inconsistent `ValueError` by using a Lock on the arrays we concatenate on.

Now, we have started to work on the feature engineering code.

We have a problem with a `Nan` value for column 5, after feature scoring using `SelectKBest(f_classif, k=10)`...

```shell
(array([ 2.13664457e+03,  3.05970593e+03,  2.35275725e+02,  2.89164262e+03,
       -6.27668700e+06,  2.71689523e+03,  2.23123122e+04,  1.61600075e+04,
        1.71411695e+04,  8.67881935e+01,  8.35089205e+01,  5.22530786e+04,
        5.43860569e+04,  1.79539777e+03,  1.79875998e+03,  6.58822038e+01,
        6.53073932e+01,  1.83736984e+04]), array([0.00000000e+00, 0.00000000e+00, 4.22489491e-53, 0.00000000e+00,
                  nan, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 1.20825541e-20, 6.34471438e-20, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 4.78779757e-16,
       6.40917066e-16, 0.00000000e+00]))
```

### Sat 6 Mai 2023

Launched the Rust program overnight. Took `1919.22s` (~30min) to parse `15332` files for `Validation`).

Why so few files ? Response: Since we have 3 directories as input, we have the compute time of only the current considered dir. But all documents were processed before. (`10727s`, around 3h for `Training`).

* [ ] Improve program time tracking.

Fixed worker panic error on key to value conversion. All JSON files in `Training` and `Validation` have their integer values represented as string, but JSON in `Performance_Test` are int in JSON.

Relaunched corrected program on `Performance_Test`, it took `292.04s` (~5min) for `1503` files.

Now, we are working on data loading in Python for feature engineering. It appears that we have a large amount of samples and labels, more that 8Gb in total.

We have a problem with loading just the part related to `Training`.

```shell
Killed
```

```shell
(base) [onyr@kenzael ~]$ grep -i 'killed process' /var/log/messages
[sudo] password for onyr: 
May  6 16:53:49 kenzael kernel: Out of memory: Killed process 47448 (python) total-vm:73810128kB, anon-rss:57310116kB, file-rss:1592kB, shmem-rss:0kB, UID:1000 pgtables:125568kB oom_score_adj:200
```

This line is a log message generated by the Linux kernel, and it indicates that a process was killed due to an out-of-memory (OOM) condition on the system. Let's break down the important parts of the log message:

* `May 6 16:53:49`: The date and time the event occurred.
* `kenzael kernel`: The hostname (kenzael) and the source of the log message (kernel).
* `Out of memory: Killed process 47448 (python)`: The reason for killing the process (out of memory) and the process ID (47448) along with the process name (python).
* `total-vm:73810128kB`: The total virtual memory used by the process (73,810,128 kB).
* `anon-rss:57310116kB`: The anonymous resident set size, which is the portion of the process's memory that is held in RAM and not backed by a file (57,310,116 kB).
* `file-rss:1592kB`: The portion of the process's memory that is backed by a file (1,592 kB).
* `shmem-rss:0kB`: The portion of the process's memory that is shared between processes (0 kB).
* `UID:1000`: The user ID (UID) of the process owner (1000).
* `pgtables:125568kB`: The size of the page tables used by the process (125,568 kB).
* `oom_score_adj:200`: The adjustment value for the process's out-of-memory score. This value is used by the kernel to determine which process to kill in case of an out-of-memory situation. A higher value makes the process more likely to be killed.

We have added multithreading for loading data and it works better. However we now have an error while trying to do the feature engineering with sklearn.

```shell
2023-05-06 18:19:45,969 - results_logger - INFO - Time elapsed since the begining of load_samples_and_labels_from_all_csv_files: 28.3767511844635 s
2023-05-06 18:19:45,977 - results_logger - INFO - Training data: 
2023-05-06 18:19:45,977 - results_logger - INFO - Number of positive labels: 6854
2023-05-06 18:19:45,977 - results_logger - INFO - Number of negative labels: 6052548
Traceback (most recent call last):
  File "/home/onyr/code/phdtrack/phdtrack_project_3/src/feature_engineering/main.py", line 41, in <module>
    main()
  File "/home/onyr/code/phdtrack/phdtrack_project_3/src/feature_engineering/main.py", line 31, in main
    pipeline_function(params, params.CSV_DATA_SAMPLES_AND_LABELS_DIR_PATH)
  File "/home/onyr/code/phdtrack/phdtrack_project_3/src/feature_engineering/feature_engineering/pipelines/univariate_feature_selection.py", line 23, in univariate_feature_selection_pipeline
    res = selector.score_func(training_samples, training_labels)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/onyr/anaconda3/envs/phdtrack-311/lib/python3.11/site-packages/sklearn/feature_selection/_univariate_selection.py", line 146, in f_classif
    X, y = check_X_y(X, y, accept_sparse=["csr", "csc", "coo"])
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/onyr/anaconda3/envs/phdtrack-311/lib/python3.11/site-packages/sklearn/utils/validation.py", line 1124, in check_X_y
    check_consistent_length(X, y)
  File "/home/onyr/anaconda3/envs/phdtrack-311/lib/python3.11/site-packages/sklearn/utils/validation.py", line 397, in check_consistent_length
    raise ValueError(
ValueError: Found input variables with inconsistent numbers of samples: [5194279, 6059402]
```

### Fri 5 Mai 2023

Launched the Rust program overnight. Took 6h to run, but failed near the end (97%) due to an error. We corrected this problem: the associated JSON file can be missing for some raw files.

Now another error appear, similar to the one we fixed on Fri 28th April.

```shell
(base) [onyr@kenzael mem_to_graph]$ cargo run -- -f /home/onyr/code/phdtrack/phdtrack_data/Validation/Validation/port-forwarding/V_8_0_P1/32/14987-1644326802-heap.raw
[...]
 Finished dev [unoptimized + debuginfo] target(s) in 0.03s
     Running `target/debug/mem_to_graph -f /home/onyr/code/phdtrack/phdtrack_data/Validation/Validation/port-forwarding/V_8_0_P1/32/14987-1644326802-heap.raw`
[2023-05-05T13:55:44 UTC][INFO mem_to_graph::params]  🚀 starting mem to graph converter
[2023-05-05T13:55:44 UTC][INFO mem_to_graph::graph_data::heap_dump_data]  📋 heap dump raw file path: "/home/onyr/code/phdtrack/phdtrack_data/Validation/Validation/port-forwarding/V_8_0_P1/32/14987-1644326802-heap.raw"
[2023-05-05T13:55:44 UTC][INFO mem_to_graph::graph_data::heap_dump_data]  📋 json file path: "/home/onyr/code/phdtrack/phdtrack_data/Validation/Validation/port-forwarding/V_8_0_P1/32/14987-1644326802.json"
[2023-05-05T13:55:44 UTC][WARN mem_to_graph::graph_annotate] key (KEY_A) found in heap dump is not the same as the key found in the json file.  
                        found aggregated_key: [177, 166, 229, 150, 194, 104, 165, 32], 
                        expected key_data.key: [177, 166, 229, 150, 194, 104, 165, 32, 11, 29, 170, 139]
[2023-05-05T13:55:44 UTC][WARN mem_to_graph::graph_annotate] key (KEY_B) found in heap dump is not the same as the key found in the json file.  
                        found aggregated_key: [224, 159, 177, 150, 129, 255, 174, 41], 
                        expected key_data.key: [224, 159, 177, 150, 129, 255, 174, 41, 23, 191, 223, 164]
[2023-05-05T13:55:46 UTC][INFO mem_to_graph::exe_pipeline]  🟢 [t: worker-9] [N°0 / 1 files] [fid: 14987-1644326802]    (Nb samples: 8737)
[2023-05-05T13:55:46 UTC][INFO mem_to_graph::exe_pipeline]  ⏱️  [chunk: 2.43s / total: 2.43s] |                    | 0.00%


```

Here, KEY_A and KEY_B are broken.

```shell
(base) [onyr@kenzael ~]$ cat /home/onyr/code/phdtrack/phdtrack_data/Validation/Validation/port-forwarding/V_8_0_P1/32/14987-1644326802.json | json_pp
{
   "ENCRYPTION_KEY_1_NAME" : "aes256-gcm@openssh.com",
   "ENCRYPTION_KEY_1_NAME_ADDR" : "55d900d6fd30",
   "ENCRYPTION_KEY_2_NAME" : "aes256-gcm@openssh.com",
   "ENCRYPTION_KEY_2_NAME_ADDR" : "55d900d6b8d0",
   "HEAP_START" : "55d900d48000",
   "KEY_A" : "b1a6e596c268a5200b1daa8b",
   "KEY_A_ADDR" : "55d900d6bf80",
   "KEY_A_LEN" : "12",
   "KEY_A_REAL_LEN" : "12",
   "KEY_B" : "e09fb19681ffae2917bfdfa4",
   "KEY_B_ADDR" : "55d900d6b120",
   "KEY_B_LEN" : "12",
   "KEY_B_REAL_LEN" : "12",
   "KEY_C" : "8e319b6d4d851254de8a743f1a12abf07586229a59b350891a87b7a514110231",
   "KEY_C_ADDR" : "55d900d4d480",
   "KEY_C_LEN" : "32",
   "KEY_C_REAL_LEN" : "32",
   "KEY_D" : "52a4623280017933d4bc90bf5cfcb918dd3cdf3af4415c42d99d7e8b5061b4bd",
   "KEY_D_ADDR" : "55d900d519b0",
   "KEY_D_LEN" : "32",
   "KEY_D_REAL_LEN" : "32",
   "KEY_E" : "",
   "KEY_E_ADDR" : "0",
   "KEY_E_LEN" : "0",
   "KEY_E_REAL_LEN" : "0",
   "KEY_F" : "",
   "KEY_F_ADDR" : "0",
   "KEY_F_LEN" : "0",
   "KEY_F_REAL_LEN" : "0",
   "NEWKEYS_1_ADDR" : "55d900d77830",
   "NEWKEYS_2_ADDR" : "55d900d777b0",
   "SESSION_STATE_ADDR" : "55d900d6e0e0",
   "SSH_PID" : "14987",
   "SSH_STRUCT_ADDR" : "55d900d6d050",
   "enc_KEY_OFFSET" : "0",
   "iv_ENCRYPTION_KEY_OFFSET" : "40",
   "iv_len_ENCRYPTION_KEY_OFFSET" : "24",
   "key_ENCRYPTION_KEY_OFFSET" : "32",
   "key_len_ENCRYPTION_KEY_OFFSET" : "20",
   "mac_KEY_OFFSET" : "48",
   "name_ENCRYPTION_KEY_OFFSET" : "0",
   "newkeys_OFFSET" : "344",
   "session_state_OFFSET" : "0"
}
```

Checking provided annotation key length:

```shell
(base) [onyr@kenzael ~]$ python
Python 3.9.13 (main, Aug 25 2022, 23:26:10) 
[GCC 11.2.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> len(bytes.fromhex("b1a6e596c268a5200b1daa8b"))
12
>>> len(bytes.fromhex("e09fb19681ffae2917bfdfa4"))
12
```

No problem from here.

Looking at the log, a half-block is missing from our aggregation.

The error comes from the computation of the number of blocks needed for the aggregation, inside `src/mem_to_graph/src/graph_annotate/mod.rs`:

```rust
let block_size = self.graph_data.heap_dump_data.as_ref().unwrap().block_size;
    for i in 0..(key_data.len / block_size) {
        let current_key_block_addr = addr + (i * block_size) as u64;
```

Since we are using the integer division, when the rest of the division is non zero, it means we need one part of the following block. To correct that, we need to round up the division if the rest is not zero.

Corrected version:

```rust
let block_size = self.graph_data.heap_dump_data.as_ref().unwrap().block_size;
    for i in 0..div_round_up(key_data.len, block_size) {
        let current_key_block_addr = addr + (i * block_size) as u64;
```

This error is related to the previous error of the 28th of April that was not fully fixed until now.

In Python, corrected program params. Added unit tests using `pytest`.

* [ ] Relaunch computations: `cargo run -- -d /home/onyr/code/phdtrack/phdtrack_data/Training/ -d /home/onyr/code/phdtrack/phdtrack_data/Validation/ -d /home/onyr/code/phdtrack/phdtrack_data/Performance_Test/`
* [ ] Clean repo
* [ ] load data

### Thu 4 mai 2023 - restarting to work on Python

Refactoring the project to work on Python.

Launching the rust program on all files with `cargo run -- -d /home/onyr/code/phdtrack/phdtrack_data/Training/ -d /home/onyr/code/phdtrack/phdtrack_data/Validation/ -d /home/onyr/code/phdtrack/phdtrack_data/Performance_Test/`

> We had to remove `__MACOSX/` folders due to errors on parsing. These files are duplicates and are of no use.

We have modified the Rust code to be able to take a list of paths, so that the generated chunks are annotated with the original folder.

We also added a test on provided path at launch.

Added basis for working on new Python project.

### Mon 1 mai 2023 - bug fix

We fixed the bug found the 30 apr and fix the special node discovery, implementing map addr to label.

### Sun 30 apr 2023 - identification of the bug (28th apr)

The error comes from the key wich aren't a multiple of 8 (block size). This lead to the aggregation of to much data. The right think to do isn't clear, and we must investigate.

### Fri 28th apr 2023 - investigating on last bugs or rust Mem2Graph

Added command line parser in the rust program. Modified the pipeline to be able to take either a file or a dir path as input.

Now, investigation on the error related to key len.

Example of broken file:

```shell
/home/onyr/code/phdtrack/phdtrack_data/Training/Training/basic/V_7_8_P1/32/3654-1643978226-heap.raw
```

Example of errors:

```shell
[2023-04-28T16:07:15 UTC][WARN mem_to_graph::graph_annotate] key (KEY_A) found in heap dump is not the same as the key found in the json file.  
                        found aggregated_key: [180, 1, 116, 30, 70, 114, 12, 163, 42, 14, 135, 60], 
                        expected key_data.key: [180, 1, 116, 30, 70, 114, 12, 163]
[2023-04-28T16:07:15 UTC][WARN mem_to_graph::graph_annotate] key (KEY_B) found in heap dump is not the same as the key found in the json file.  
                        found aggregated_key: [91, 254, 235, 104, 52, 221, 95, 47, 195, 17, 20, 233], 
                        expected key_data.key: [91, 254, 235, 104, 52, 221, 95, 47]
```

Inside the associated json:

```shell
(base) [onyr@kenzael mem_to_graph]$ cat /home/onyr/code/phdtrack/phdtrack_data/Training/Training/basic/V_7_8_P1/32/3654-1643978226.json | json_pp
{
   "ENCRYPTION_KEY_1_NAME" : "aes256-gcm@openssh.com",
   "ENCRYPTION_KEY_1_NAME_ADDR" : "563ae7de5250",
   "ENCRYPTION_KEY_2_NAME" : "aes256-gcm@openssh.com",
   "ENCRYPTION_KEY_2_NAME_ADDR" : "563ae7de4280",
   "HEAP_START" : "563ae7dda000",
   "KEY_A" : "b401741e46720ca32a0e873c",
   "KEY_A_ADDR" : "563ae7de4fc0",
   "KEY_A_LEN" : "12",
   "KEY_A_REAL_LEN" : "12",
   "KEY_B" : "5bfeeb6834dd5f2fc31114e9",
   "KEY_B_ADDR" : "563ae7de7a10",
   "KEY_B_LEN" : "12",
   "KEY_B_REAL_LEN" : "12",
   "KEY_C" : "fbfcd9b57c493dcd35b42dcbb5d217cab3ac084f59ecdffce1acad9f638f61ef",
   "KEY_C_ADDR" : "563ae7de5020",
   "KEY_C_LEN" : "32",
   "KEY_C_REAL_LEN" : "32",
   "KEY_D" : "3386b72857694ab7d2121adbaaf94ea5c4ac2e09afbc35c4d58683d7c8edb44a",
   "KEY_D_ADDR" : "563ae7de9d80",
   "KEY_D_LEN" : "32",
   "KEY_D_REAL_LEN" : "32",
   "KEY_E" : "",
   "KEY_E_ADDR" : "563ae7de6010",
   "KEY_E_LEN" : "0",
   "KEY_E_REAL_LEN" : "0",
   "KEY_F" : "",
   "KEY_F_ADDR" : "563ae7dea950",
   "KEY_F_LEN" : "0",
   "KEY_F_REAL_LEN" : "0",
   "NEWKEYS_1_ADDR" : "563ae7dec5c0",
   "NEWKEYS_2_ADDR" : "563ae7dec6c0",
   "SESSION_STATE_ADDR" : "563ae7de6ef0",
   "SSH_PID" : "3654",
   "SSH_STRUCT_ADDR" : "563ae7de6670",
   "enc_KEY_OFFSET" : "0",
   "iv_ENCRYPTION_KEY_OFFSET" : "40",
   "iv_len_ENCRYPTION_KEY_OFFSET" : "24",
   "key_ENCRYPTION_KEY_OFFSET" : "32",
   "key_len_ENCRYPTION_KEY_OFFSET" : "20",
   "mac_KEY_OFFSET" : "48",
   "name_ENCRYPTION_KEY_OFFSET" : "0",
   "newkeys_OFFSET" : "344",
   "session_state_OFFSET" : "0"
}
```

It appears that the annotations for key length of KEY_A and KEY_B is true:

```shell
>>> len(bytes.fromhex("3386b72857694ab7d2121adbaaf94ea5c4ac2e09afbc35c4d58683d7c8edb44a"))
32
>>> len(bytes.fromhex("b401741e46720ca32a0e873c")) # KEY_A
12
```

When trying to Rust code in a Jupyter kernel, we get:

```rust
:dep hex = "0.4"
use hex;

let key_hex = "b401741e46720ca32a0e873c"; // KEY_A
let key_bytes: Vec<u8> = hex::decode(key_hex).unwrap();
println!("key_bytes: {:?}", key_bytes);
println!("key_bytes len: {} {}", key_bytes.len(), "bytes")
```

```shell
key_bytes: [180, 1, 116, 30, 70, 114, 12, 163, 42, 14, 135, 60]
key_bytes len: 12 bytes
```

Which is still correct.

```shell
found aggregated_key: [180, 1, 116, 30, 70, 114, 12, 163, 42, 14, 135, 60], 
expected key_data.key: [180, 1, 116, 30, 70, 114, 12, 163]
```

It turns out we had inverted the print of `key_data.key` from the json and the `aggregated_key`. So the real problem comes from the aggregation process of blocks forming the key.

* [ ] Investigate and fix the aggregation of key data blocks into a real value of key.
* [ ] Fix the special pointer annotation.

### Mon 24th apr 2023

I launched the program during the night, but it failed at about 30% due to an unwrap on a None value. We investigated the issue, and it appears that this comes from the processing of JSON annotation files. Some of them are incomplete, and do not have the necessary keys we need.

Example of wrong JSON file: `/home/onyr/code/phdtrack/phdtrack_data/Training/Training/basic/V_6_2_P1/16/12847-1644307405.json`:

```json
{
    "ENCRYPTION_KEY_NAME": "aes for femb * size >cdsa curve doesn't matchrestore old [e]gid", 
    "ENCRYPTION_KEY_LENGTH": "16", 
    "KEY_C": "e231ee54a3311c8570316162fd73aafb", 
    "KEY_D": "fe6d048d7cc569a6413950e9d443f6bb", 
    "HEAP_START": "56064e1a4000"
}
```

We have added error handling for this situation.

```shell
[2023-04-24T16:33:18 UTC][WARN mem_to_graph::exe_pipeline]  🔴 [N°57094 / 86760 files] [id: 30555-1644309926-heap.raw]    Missing JSON key: KEY_C_ADDR[2023-04-24T16:33:18 UTC][WARN mem_to_graph::exe_pipeline]  🔴 [N°57094 / 86760 files] [id: 30555-1644309926-heap.raw]    Missing JSON key: KEY_C_ADDR
```

* [ ] Fix invalid special node like SESSION_STATE_NODE...
* [ ] Check invalid keys, investigate if we did mistakes with key lenght processing (node gathering, computing...). Do we check the key lenght in the JSON file ?

### Thu 20th apr 2023

Working on sample generation pipeline from many files given a folder as input. The rust pipeline is able to detect all `-heap.raw` files of nested sub-directories, given a base directory. It call the samples and labels generation by chunks and save every chunks into its own file of results.

We even added time logging and a progress bar.

```shell
[2023-04-20T15:14:48Z INFO  mem_to_graph::graph_data::heap_dump_data]  📋 heap dump raw file path: "/home/onyr/code/phdtrack/phdtrack_data/Training/Training/port-forwarding/V_8_0_P1/16/13263-1644324152-heap.raw"
[2023-04-20T15:14:48Z INFO  mem_to_graph::graph_data::heap_dump_data]  📋 heap dump raw file path: "/home/onyr/code/phdtrack/phdtrack_data/Training/Training/port-forwarding/V_8_0_P1/16/13885-1644324152-heap.raw"
[2023-04-20T15:14:48Z INFO  mem_to_graph::graph_data::heap_dump_data]  📋 heap dump raw file path: "/home/onyr/code/phdtrack/phdtrack_data/Training/Training/port-forwarding/V_8_0_P1/16/13760-1644324152-heap.raw"
[2023-04-20T15:14:48Z INFO  mem_to_graph::graph_data::heap_dump_data]  📋 heap dump raw file path: "/home/onyr/code/phdtrack/phdtrack_data/Training/Training/port-forwarding/V_8_0_P1/16/12490-1644324152-heap.raw"
[2023-04-20T15:14:48Z INFO  mem_to_graph::graph_data::heap_dump_data]  📋 heap dump raw file path: "/home/onyr/code/phdtrack/phdtrack_data/Training/Training/port-forwarding/V_8_0_P1/16/13028-1644324152-heap.raw"
[2023-04-20T15:14:48Z INFO  mem_to_graph::graph_data::heap_dump_data]  📋 heap dump raw file path: "/home/onyr/code/phdtrack/phdtrack_data/Training/Training/port-forwarding/V_8_0_P1/16/12607-1644324152-heap.raw"
[2023-04-20T15:14:48Z INFO  mem_to_graph::graph_data::heap_dump_data]  📋 heap dump raw file path: "/home/onyr/code/phdtrack/phdtrack_data/Training/Training/port-forwarding/V_8_0_P1/16/12733-1644324152-heap.raw"
[2023-04-20T15:14:48Z INFO  mem_to_graph::graph_data::heap_dump_data]  📋 heap dump raw file path: "/home/onyr/code/phdtrack/phdtrack_data/Training/Training/port-forwarding/V_8_0_P1/16/12392-1644324152-heap.raw"
[2023-04-20T15:14:48Z INFO  mem_to_graph::graph_data::heap_dump_data]  📋 heap dump raw file path: "/home/onyr/code/phdtrack/phdtrack_data/Training/Training/port-forwarding/V_8_0_P1/16/14668-1644324152-heap.raw"
[2023-04-20T15:14:48Z INFO  mem_to_graph::graph_data::heap_dump_data]  📋 heap dump raw file path: "/home/onyr/code/phdtrack/phdtrack_data/Training/Training/port-forwarding/V_8_0_P1/16/13305-1644324152-heap.raw"
[2023-04-20T15:14:51Z INFO  mem_to_graph::exe_pipeline]  🟢 [N°576 / 86760 files] [id: 12733-1644324152]    (Nb samples: 8733)
[2023-04-20T15:14:51Z INFO  mem_to_graph::exe_pipeline]  🟢 [N°571 / 86760 files] [id: 12490-1644324152]    (Nb samples: 8734)
[2023-04-20T15:14:51Z INFO  mem_to_graph::exe_pipeline]  🟢 [N°574 / 86760 files] [id: 12392-1644324152]    (Nb samples: 8733)
[2023-04-20T15:14:51Z INFO  mem_to_graph::exe_pipeline]  🟢 [N°573 / 86760 files] [id: 13028-1644324152]    (Nb samples: 8734)
[2023-04-20T15:14:51Z INFO  mem_to_graph::exe_pipeline]  🟢 [N°578 / 86760 files] [id: 13305-1644324152]    (Nb samples: 8734)
[2023-04-20T15:14:51Z INFO  mem_to_graph::exe_pipeline]  🟢 [N°570 / 86760 files] [id: 13885-1644324152]    (Nb samples: 8735)
[2023-04-20T15:14:52Z INFO  mem_to_graph::exe_pipeline]  🟢 [N°577 / 86760 files] [id: 12607-1644324152]    (Nb samples: 8733)
[2023-04-20T15:14:52Z INFO  mem_to_graph::exe_pipeline]  🟢 [N°572 / 86760 files] [id: 13760-1644324152]    (Nb samples: 8734)
[2023-04-20T15:14:52Z INFO  mem_to_graph::exe_pipeline]  🟢 [N°575 / 86760 files] [id: 13263-1644324152]    (Nb samples: 8734)
[2023-04-20T15:14:52Z INFO  mem_to_graph::exe_pipeline]  🟢 [N°579 / 86760 files] [id: 14668-1644324152]    (Nb samples: 8734)
[2023-04-20T15:14:52Z INFO  mem_to_graph::exe_pipeline]  ⏱️  [chunk: 3.82s / total: 34.60s] |                    | 0.66%
```

### Wed 19th apr 2023

Worked on sample generation from the graph. We have added a parameter to activate or not the edge compression. But it appears that this compression is probably meaningless in our case since we need the graph structure in order to generate meaningfull samples.

### Tue 18th apr 2023

Continued to work on the graph annotation pipeline. We added the code for key annotation and the associated tests.

### Fri 14th apr 2023

Finally finished graph_data after weeks of hard work. We have tested the graph creation process. We also have added 2 differents ways of creating edges, one doing a compression of data, by wrapping chains of pointers. This make the final graph having no links between data structures since intermediate pointer to pointer links are missing.

We then started to work on graph_annotate, added the code to get the key data inside heap_dump_data (to load key data at json loading, only once contrary to Python). The base pipeline for annonation is already implemented for SSH_STRUCT and SESSION_STATE.

* [ ] add the pipeline for key annotation
* [ ] add the code to generate samples and labels

### Thu 13th apr 2023

Investigating on the graph structure generation. I have corrected the formatter of the graph, added code to save it to a file and have been working on a Python script to clean and generate images from the .gv file.

### Wed 12th apr 2023

We continued to work on graph_data correction and testing. We have tried to find a datastructure by hand from the heap dump raw file, but we couldn't find it in our results from file parsing. We now need to investigate the issue.

> It is highly probable that the issue is related to nested data structures. Actually, our code doesn't work for nested data structures!

### Tue 11th Apr 2023

Finished to debug the immutable and mutable and lifetime errors due to the edges having references of nodes. Now, edges have real addresses as u64 which greatly simplifies the code.

I rewrote the pointer parsing workflow, but some testing and debugging is needed.

* [ ] debug the pointer parsing workflow
* [ ] test the pointer parsing workflow

### Mon 10th april 2023 (and week before)

We finally managed to get out of the endianness hell. The idea was to simply remove the endianness param from the function that is supposed to convert a str intp a block of bytes. Now, we are facing a design problem. We cannot chain mutable references in rust, contrary to python, so no possibility to have several function doing some chained calls on different mutability variants of self.

* [X] Rewrite the constructor to move from internal function to external function (no more need)
* [X] fix the borrowing problem.

### Fri 31st mar 2023

Need to change our graph data structure with a [GraphMap](https://docs.rs/petgraph/0.5.0/petgraph/graphmap/struct.GraphMap.html), so as to be able to have a test for edge existence in constant time.

More ressources: [GraphMap doc](https://docs.rs/petgraph/0.5.0/petgraph/graphmap/struct.GraphMap.html), [Introduction to PetGraph](https://depth-first.com/articles/2020/02/03/graphs-in-rust-an-introduction-to-petgraph/)

BIG refactor needed. Need to have a Map of `NodeIndex <u64>` to `Node`, where `u64` is an address in the heap dump. The graph is then filled with `u64` and edges with more complex data.

The annotation of type and data for `u64` graph vertices happen through the map.

The hash function should be actually sending back the address.

### Tue 28th mar 2023

Continuing to work on Rust code version.

### Mon 27th mar 2023

Started to rework the `mem_graph` python sub-module in Rust. We have tested to generate bindings using `pyo3` rust crate. We then switched to rewrite `heap_dump_data.py`. In order to make sure we reimplement the code according to what we did in Python, we are using TDD on the Rust project.

The tests and code is already working for `heap_dump_data.rs`.

* [X] Continue to rewrite components in Rust, for improved security and speed.
* [ ] WARN: Python `is_pointer()` is dead broken code, determine how to check that a block content is a pointer !

### Wed 22th mar 2023

Restarted to work on the project. Clément added some code and a Logger, but a lot of debugging is needed.

Rust improvements

* [ ] Compute number of nodes (VN and PN) just after creation of a DTN node.
* [ ] While loading vectorization results (features and labels), calculate all the features one time with max depths, then save differents depths from there instead of computig several times.

notes about current compute time:

```shell
Time elapsed since the begining of load_files_and_gen_samples_and_labels from 1065 heap dump files: 5273.103894233704 s (~= 1h30 / 1065 files, or ~= 5s / heap dump file)
```

### Sat 25th feb 2023

* [ ] beautify graph representation

### Fri 24th feb 2023

* [X] begining the implementation of simplification of the graph
* [X] debugging the simplification of the graph

### Tue 21th Feb 2023

* [X] finishing and debuging the logging

### Mon 21th Feb 2023

To make the casual logging, use RotatingFileHandler ([here](https://stackoverflow.com/questions/40088496/how-to-use-pythons-rotatingfilehandler)).

* [X] refactoring and clean code
* [X] beginning the implementation of logging

### Fri 17th Feb 2023

We have ideas for many improvements. We have worked on the high recall training pipeline, as well as other refactoring stuff. We have added an command line argv parser.

* [ ] create a training and testing log system, to keep track of both result, but ESPECIALLY training parameters. The number of samples is missing ! create a proper logger, using the standard library of Python. At least 2 loggers are necessary. Both loggers write to the terminal. One logs all messages to rotating log files (can use 20 files of 50Mb), the other log 1 file per model evaluation (1 eval == 1 file), including training and testing params, file number, depth, provenance of files...
* [X] add exe command line flags to control training and testing.
* [ ] new potential features "ValueNode position" and "related data structure size". Note that we think that adding such features is possibly wrong, since our approach tries to hide any information about the addresses, including address ordering. This can also affect the generality of the model, since the size of the keys, hence the ordering and position of keys in heap dump block may differ and surspecialize the model.
* [ ] refactor the code (depht to file name), ...
* [ ] Investigate why the samples and labels generation is so slow. Idea: limit the number of simultaneous thread, we think we are RAM memory bound... We have already made a lot of refactoring
* [X] make another classifier with high recall
* [ ] make bigger model (use more data).

### Thu 16th Feb 2023

We debugged the ML training process and added multi-threading to both the loading/generation of samples and lables, and the classifier fitting. We also did a lot of refactoring around the data loading pipeline.

* [X] debug ML training
* [X] Start working on ML detection of keys
* [X] find how to vectorize graph or node
* [X] pipeline for the model evaluation
* [ ] refactor the code (depht to file name), ...
* [ ] Investigate why the samples and labels generation is so slow. Idea: limit the number of simultaneous thread, we think we are RAM memory bound...
* [ ] make another classifier with high recall
* [ ] make bigger model (use more data).
* [ ] add exe command line flags to control traning and testing.
* [ ] create a proper logger, using the standard library of Python. At least 2 loggers are necessary. Both loggers write to the terminal. One logs all messages to rotating log files (can use 20 files of 50Mb), the other log 1 file per model evaluation (1 eval == 1 file), including training and testing params, file number, depth, provenance of files...

### Wed 15th Feb 2023

We discovered a problem with pointers pointing to data structures, since they do not really points to the data structure malloc header (DataStructureNode), but instead, to the first block after it. This means our current representation is wrong and do not make possible to really understand links between data structures.

The data structures addresses given in the JSON file are neither the malloc header address of the data stucture nor the first block after a malloc header. It is in fact the address of a pointer pointing to the data structure!

* [X] Refactor the PointerNode and ValueNode classes.
* [X] Correct graph representation
* [X] Correct JSON data annotation
* [ ] debug ML training
* [ ] Start working on ML detection of keys
* [ ] find how to vectorize graph or node

##### About Node Embedding and Feature Engineering

[Introduction to Node Embedding](https://memgraph.com/blog/introduction-to-node-embedding) ⭐️

[Graph Embeddings: How nodes get mapped to vectors](https://towardsdatascience.com/graph-embeddings-how-nodes-get-mapped-to-vectors-2e12549457ed)

[Graph Embeddings — The Summary](https://towardsdatascience.com/graph-embeddings-the-summary-cc6075aba007)

[neo4j graph embeddings](https://neo4j.com/docs/graph-data-science/current/machine-learning/node-embeddings/)

[scikit-network](https://scikit-network.readthedocs.io/en/latest/index.html)

Because we are working on a custom graph, representing a precise data structure, we think that rely on **Random Walk based** or **Deep Learning based** will not preserve enough the specificities of the graph we have. So the best idea now is to do some Feature Engineering to generate our own node vector representation that we can easily label. Because what we want to predict is just the address of the key, and because the keys are of different possible lenght, we will only keep the address of the first block.

* [X] Refactor KeyNode, so that when we keep it for visualization step, but we need not to remove the other ValueNodes, the non-first key data ValueNodes. We want our ML model to find only the KeyNode, i.e. the address of the first block of the keys.
* [X] create pipeline for embedding
* [ ] create training ML pipeline
* [ ] create ML evaluation pipeline

Features idea, for ValueNodes only

* number of input ancestor node, by type, of a given depth. The depth is an hyper-param. Considering the relative small size of the structure, a small int, like 5 or 10 should be enough. This representation take in consideration the very directive structure of the graph.

### Tue 14th Feb 2023

We started to try to visualize our first results concerning the data structure generation. To do so, we tried different softwares (see potential DOT visualizers [here](https://stackoverflow.com/questions/3433655/free-visual-editor-for-graph-dot-files) and [here](https://linuxhint.com/kgrapheditor-linux/)), but most of them are broken. We then generated directly a visualization using the following command line:

```shell
sfdp -Gsize=67! -Goverlap=prism -Tpng 467-1644391327-heap.gv > 467-1644391327-heap-sfdp.png
```

This uses directly Graphviz, more info [in the doc](https://graphviz.org/Gallery/undirected/root.html), other types of visualizations [here](https://graphviz.org/gallery/).

New types:

* [ ] Link json data to our rebuild datastructures:
* [X] get JSON key addresses and lenghts
* [X] get key structures from JSON
* [ ] get encoding string data and make custom representation
* [ ] match all data with generated graph
* [X] make beautiful colored graph, refactor graph edge annotations
* [ ] link C code structures to our rebuilt data structures

ML thinking: Now that we have our annoted graph, we need to feed it to a ML model. We could for instance find a vector representation for each node of the graph, annotate it, then feed that to the model, and see the results.

The problem is that we have an imbalaced dataset with very few positive values. We need to filter out useless structs to limit the number of nodes.

### Mon 13th Feb 2023

We restarted to work on the project. We are currently implementing the data structure detection and recreation loop.

We DO NOT CURRENTLY works on the edges outside of datastructures (we don't follow the pointers yet).

* [X] Test current code.
* [X] Need to do step 2: follow the pointers

We then debugged and worked on the step two: following the pointers identified inside the data structures. If the pointers points to already discovered nodes inside data structures, we plot them, otherwise, we create new nodes and follow them if they are pointers.

* [ ] Need to further test step 2

### Tue 31th Jan 2023

look at malloc headers (in little endian format) to determine the lenght (number of block)

graph -> generate representation

* [ ] Finish to refactor the python module
* [ ] Use NetworkX to generate and [display graphs](https://networkx.org/documentation/stable/reference/drawing.html#module-networkx.drawing.nx_agraph)
* [ ] Create functions to identify data-structures and lonely pointers (see pictures)

Data representation to implement: The idea is to try to follow all possible datastructures.

![img 1](./img/worklog/IMG_9370.jpg)

![img 2](./img/worklog/IMG_9371.jpg)

The firtst node of a structure is a blank node. It represents the first byte block after the malloc header. It can be a piece of data or a pointer. Other pointers inside the data structures are linked to this blank node via *data structure link.*

### Thu 26th Jan 2023

Started to think about the new representation of memory data structures into a graph representation.

Read SSHkey_vm_introspection, and looking at [OpenSSH-Portable](https://github.com/openssh/openssh-portable). Here are our notes:

[packet.h](https://github.com/openssh/openssh-portable/blob/master/packet.h) contains `struct ssh`:

* 14 pointers
* 4 int

[packet.c](https://github.com/openssh/openssh-portable/blob/master/packet.c) contains `struct session_state`:

* 13 pointers
* 17 int
* 4 `u_int`
* 1 `u_int64_t`
* 1 `u_int32_t`
* 1 `time_t`
* 1 `u_char`
* 1 `size_t `

> There is a pointer from `ssh` to `session_state`

[kex.h](https://github.com/openssh/openssh-portable/blob/master/kex.h) contains `struct newkeys`:

```c
struct newkeys {
	struct sshenc	enc;
	struct sshmac	mac;
	struct sshcomp  comp;
};

```

sshenc:

* 4 pointers
* 1 `int`
* 3 `u_int`

sshmac inside [mac.h](https://github.com/openssh/openssh-portable/blob/master/mac.h):

* 4 pointers
* 3 `int`
* 2 `u_int`

sshcomp:

* 1 pointer
* 1 `u_int`
* 1 `int`

We suppose the top level struct contains the sum of all bytes of its sub-structures.

We also spent some time to investigate who are currently maintaining and extending this project. It is 4 google engineer since 1999 : [Damien Miller](https://www.linkedin.com/in/djmdjm/), [Darren Tucker](https://www.linkedin.com/in/dtucker/), [Markus Friedl](https://www.linkedin.com/in/markus-friedl-6709861/), [Niels Provos](https://www.linkedin.com/in/nielsprovos/)

### Wed 25th Jan 2023

Started to look at the advanced graph generation. Lot's of work to do:

* [ ] Complete pointer to pointer data structure linking, using `malloc` data store before pointed value.
* [ ] Transition from DOT graph generation to NetworkX.

### Thu 19th Jan 2023

We worked on displaying the graph of pointers. We removed unique-vertice graphs. We tried to check what the pointed data.

* [ ] Refactor functions out of Notebook
* [ ] Fix graphviz strange " error
* [ ] Fix utf-8 incorrect formatting.

### Tue 17th Jan 2023

Finally corrected the pointer extraction script. Pointers are coded using LITTLE-ENDIAN ordering.

* [X] Graphs generated are too big. Need to remove 1, or 2 nodes graphs. Refactoring needed.

### Mon 16th Jan 2023

Trained a high recall SVC classifier using cross validation and grid search.

### Sun 15th Jan 2023

Started to build a script to get pointers from raw heap dump files.

### Sat 14th Jan 2023

Working on obtaining Keys from raw heap dump files. Trained new classifiers from dataset.

### Fri 13th Jan 2023

Started to look at raw data using Okteta, which is a hex viewer to view the data. Install on Fedora with `sudo yum install okteta`. I have tried to see if I could locate the keys manually using Okteta without success.

* [X] How to find the keys in Okteta? Okteta broken, use VIM and `:` then `%!xxd` to search for patterns and bytes.
* [X] How to search the HEAP_START? I can't find it in Okteta?
* [ ] How to create a dataset from the given data files?
* [ ] Where are the `-key.log` files necessary for training? Do we need to adapt the code to works with the provided `.json` files instead?
* [ ] Follow the pointers in mem and create a DOT graph with a Python script. Use .json solutions as starting point.

Questions ?

* [X] How to use create_dataset(), and create_splits...
* [X] where are the -key.log (-> try to generate them to test)
* [ ] Why is the no `basic` in `TYPES = ["client-side", "dropbear", "OpenSSH", "port-forwarding", "scp", "normal-shell"]` (constants.py), whereas there are folders called `basic` from Zenodo datasets. Same for \`client` ?

### Thu 12th Jan 2023

Finished baseline of heavy refactoring. Original code working in both DEPLOY and non DEPLOY mode.

* [ ] Use and modify `train_classifier` to work with different classifiers. Continue to work on the testzone.

### Wed 11th Jan 2023

Restarted to work on PhDTrack project. Reread documents and research materials. Continuing to work on code refactoring.
