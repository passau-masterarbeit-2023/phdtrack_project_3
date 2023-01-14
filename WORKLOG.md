# Worklog

### Fri 13th 2023

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

### Thu 12th 2023

Finished baseline of heavy refactoring. Original code working in both DEPLOY and non DEPLOY mode.

* [ ] Use and modify `train_classifier` to work with different classifiers. Continue to work on the testzone.

### Wed 11th 2023

Restarted to work on PhDTrack project. Reread documents and research materials. Continuing to work on code refactoring.
