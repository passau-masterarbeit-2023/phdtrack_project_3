# Worklog

look at malloc headers (in little endian format) to determine the lenght (number of block)

graph -> generate representation

### Tue 14th Feb 2023

We started to try to visualize our first results concerning the data structure generation. To do so, we tried different softwares (see potential DOT visualizers [here](https://stackoverflow.com/questions/3433655/free-visual-editor-for-graph-dot-files) and [here](https://linuxhint.com/kgrapheditor-linux/)), but most of them are broken. We then generated directly a visualization using the following command line:

```shell
sfdp -Gsize=67! -Goverlap=prism -Tpng 467-1644391327-heap.gv > 467-1644391327-heap-sfdp.png
```

This uses directly Graphviz, more info [in the doc](https://graphviz.org/Gallery/undirected/root.html), other types of visualizations [here](https://graphviz.org/gallery/).

New types:

* [ ] Link json data to our rebuild datastructures:
* [ ] get JSON key addresses and lenghts
* [ ] get key structures from JSON
* [ ] get encoding string data and make custom representation
* [ ] match all data with generated graph
* [X] make beautiful colored graph, refactor graph edge annotations




* [ ] link C code structures to our rebuilt data structures

### Mon 13th Feb 2023

We restarted to work on the project. We are currently implementing the data structure detection and recreation loop.

We DO NOT CURRENTLY works on the edges outside of datastructures (we don't follow the pointers yet).

* [X] Test current code.
* [X] Need to do step 2: follow the pointers

We then debugged and worked on the step two: following the pointers identified inside the data structures. If the pointers points to already discovered nodes inside data structures, we plot them, otherwise, we create new nodes and follow them if they are pointers.

* [ ] Need to further test step 2

### Tue 31th Jan 2023

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
