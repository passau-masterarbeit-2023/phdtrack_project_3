# Worklog: Rust embeddings

## Objectives

> Create a new embedding focused on datastructure embedding.

Create an embedding focused on encapsulating the data structures. What we want is to vectorize the data structure in a syntetic way. 

Below are our stating ideas for semantic data structure embedding:

* Use the number of bytes (upper bound)
* Nb of pointers inside
* Nb of ancestor and children DNT and VN, recursively with a hyperparameter being the depth (probably between 4 and 8)

## Work
