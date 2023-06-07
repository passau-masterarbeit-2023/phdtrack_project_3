# Worklog 2

## Meetings

### Meeting 30th Mai 2023

* [X] What is the 9th byte after the malloc header ? We could not really see it.

Christopher: We don't care so much about understanding and programming a specific code for managing malloc header, since the malloc header is heavily dependant on the architecture and implementation. You should just drop the flags and recover only an upper bound of the size of the data structure.

* [X] Separation of work

Two tasks: one is ML for KeyNode detection, the second one if the development of a new embedding focused on datastructure embedding.

> Each of us must write in his own style, we cannot copy any text from one another.

* [X] research paper

Yes, potentially 2 papers on this

* [X] access to computing machines

Incoming

##### notes about meeting of 1st of June

Planning: end of experiment part, end of July.

Writing: August

Submission: end of August

Final: end of September

### Meeting 1st June 2023

Seperation of work:

* Clément: need to write on embedding, specifically about data structure embedding
* Florian: need to write on ML, specifically on Key Node prediction
* Both of us will need to write about the modeling (rust code)

Improvement of ML precision:

Christopher and Michael have bette results on the precision, because they provide the classifier with less information, more focused about the related Data Structure of the node. A good assumption is to say that we can uniquely identify Data Structures by their number of pointers.

* [ ] Try to learn classifiers on a subset of the samples, with only DTN information after the initial Key Prediction with high recall classifier, so as to increate the general performance.

## Work

### Fri 2 Jun 2023

* [ ] make common the base of the params (logging) and the base of the result manager (some base info like time)

### Tue 30 Mai 2023

Meeting with Christopher. We need to continue the work on ML part for KeyNode detection, and create a new embedding focused on data structures.

Made refactoring and cleaning on `.env` params in the Rust.

### Fri 26 Mai 2023

* [X] Finish to read Christopher's code
* [X] Need to test the refactoring with new params
* [ ] Add new param "DATA_BALANCING" and modify the pipelines (priority)
* [ ] complete the integration of result keeping, and test/debug
* [ ] Complete result keeping integration, for now, only start time and pipeline names are provided.
* [ ] create a meta-script that launch and test the program with all possible combination of program command lines

Heavy refactoring. We reworked the project to be able to handle different training and testing datasets. We also did some corrections and tested the program with a wide range of parameters.

### Wed 24 Mai 2023

Started to read Christopher python code for graph extraction. We then realized that we were not handling correcly the memalloc flag, and made some correction into the rust code.

### Wed 17 Mai 2023

* [ ] Create new pipelines for `SGDClassifier` and `MLPClassifier`.
* [ ] Create a pipeline with a RandomForest on chuncks and a classifier on the result of RandomForest for improving precision.
* [ ] Do a grid search on `RandomForest`
* [ ] Add a mecanism to keep results inside a CSV
* [ ] Transform that (CSV table of results) into a table in latex.
* [ ] Improve result logs, include results, data origin, classifier name...
* [X] Split training and testing (update CLI params)
* [ ] Add logging for feature engineering through CSV

##### pipeline for `SGDClassifier`

We have added our first pipeline with both partial and total fitting for a `SGDClassifier`.

Here are results for **partial fitting** on `validation`:

```shell
(phdtrack-311) [onyr@kenzael feature_engineering]$ python main.py -p ml_sgd -o validation -b
🚀 Running program...
Passed program params:
param[0]: main.py
param[1]: -p
param[2]: ml_sgd
param[3]: -o
param[4]: validation
param[5]: -b
Program paths are OK.
2023-05-17 09:19:00,387 - results_logger - INFO - Program params:   [see below]
2023-05-17 09:19:00,387 - results_logger - INFO -       debug: False
2023-05-17 09:19:00,387 - results_logger - INFO -       max_ml_workers: 10
2023-05-17 09:19:00,395 - common_logger - INFO - Running pipeline: ml_sgd
2023-05-17 09:19:00,395 - results_logger - INFO - timer for pipeline (ml_sgd) started
[...]
2023-05-17 09:19:46,386 - common_logger - INFO - 📋 [f: 153 / 154] Loading file /home/onyr/code/phdtrack/phdtrack_project_3/src/mem_to_graph/data/samples_and_labels/Validation__chunck_idx-118_samples.csv 
2023-05-17 09:19:46,446 - results_logger - INFO - Removing 1 columns with only one unique value: ['f_dtns_ancestor_1']
2023-05-17 09:19:46,613 - common_logger - INFO - Number of empty files: 24
2023-05-17 09:19:50,467 - results_logger - INFO - Precision: 0.0033172557660275164, Recall: 0.6098213583064452, F1-score: 0.006598616921718383
2023-05-17 09:19:50,471 - results_logger - INFO - Time elapsed since the begining of pipeline (ml_sgd): 50.0751838684082 s
```

The precision is really low: 0.003, the recall is better: 0.61.

Here is another run with **one time fitting** on `validation`:

```shell
(phdtrack-311) [onyr@kenzael feature_engineering]$ python main.py -p ml_sgd -o validation
🚀 Running program...
Passed program params:
param[0]: main.py
param[1]: -p
param[2]: ml_sgd
param[3]: -o
param[4]: validation
Program paths are OK.
2023-05-17 09:20:27,259 - results_logger - INFO - Program params:   [see below]
2023-05-17 09:20:27,259 - results_logger - INFO -       debug: False
2023-05-17 09:20:27,259 - results_logger - INFO -       max_ml_workers: 10
2023-05-17 09:20:27,261 - results_logger - INFO - timer for load_samples_and_labels_from_all_csv_files started
[...]
2023-05-17 09:20:30,499 - results_logger - INFO - 📋 [153/154] Loading samples and labels from /home/onyr/code/phdtrack/phdtrack_project_3/src/mem_to_graph/data/samples_and_labels/Validation__chunck_idx-118_samples.csv
2023-05-17 09:20:30,711 - common_logger - INFO - Number of empty files: 24
2023-05-17 09:20:31,050 - results_logger - INFO - Time elapsed since the begining of load_samples_and_labels_from_all_csv_files: 3.789315700531006 s
2023-05-17 09:20:31,869 - results_logger - INFO - Removing 1 columns with only one unique value: ['f_dtns_ancestor_1']
2023-05-17 09:20:32,189 - results_logger - INFO - Loaded data (validation)
2023-05-17 09:20:32,189 - results_logger - INFO - Number of positive labels: 63743
2023-05-17 09:20:32,189 - results_logger - INFO - Number of negative labels: 24432867
2023-05-17 09:20:32,189 - common_logger - INFO - Running pipeline: ml_sgd
2023-05-17 09:20:32,190 - results_logger - INFO - timer for pipeline (ml_sgd) started
2023-05-17 09:20:44,956 - results_logger - INFO - Precision: 0.0044399446805125226, Recall: 0.642080378250591, F1-score: 0.008818907182841878
2023-05-17 09:20:44,961 - results_logger - INFO - Time elapsed since the begining of pipeline (ml_sgd): 12.7716383934021 s
```

With one time fitting, the results are slightly better, with a precision of: 0.004, and a recall: 0.64.

### Tue 16 Mai 2023

* [X] refactor with data batches
* [X] refactor the check with parallel read-only checks
* [ ] Create new pipelines for `SGDClassifier` and `MLPClassifier`.

We have refactored the code to work with data batches. However, not all the classifiers support partial fitting. Classifiers that don't support it still require to load all the data at once. We do it by consumming the generator.

The following classifiers on classification problems are:

```shell
MultinomialNB
BernoulliNB
Perceptron
SGDClassifier
PassiveAggressiveClassifier
MLPClassifier
...
```

For our problem, since we try to maximize the recall (we want to detect all possible keys), here are the interesting classifiers to try:

1. `SGDClassifier`: Stochastic Gradient Descent (SGD) is a linear classifier optimized by stochastic gradient descent. It can handle large-scale data and allows you to control the trade-off between precision and recall using the `loss` parameter. For instance, setting `loss="log"` gives a logistic regression, which can provide good performance on binary classification problems.
2. `PassiveAggressiveClassifier`: This classifier is a margin-based online learning algorithm for binary classification. It might be helpful if your data stream has a lot of noise or your positive and negative classes are not linearly separable.
3. `Perceptron`: This is a simple algorithm suitable for large scale learning. It's fast and could be a good starting point for binary classification problems. However, it may not perform as well as other, more complex models if your data is not linearly separable.
4. `BernoulliNB`, `MultinomialNB`, `GaussianNB`: These are Naive Bayes classifiers. Naive Bayes classifiers are a family of simple "probabilistic classifiers" based on applying Bayes' theorem with strong independence assumptions between the features. They can be a good choice if your features are conditionally independent given the class. BernoulliNB and MultinomialNB are often used for text data, while GaussianNB is used for numerical data.
5. `MLPClassifier`: This is a multi-layer perceptron classifier, which is a type of neural network. It can model more complex relationships between the features and the target variable, and might be suitable if your data is not linearly separable. However, it can require more computational resources and might be slower to train than some other classifiers.

### Mon 15 Mai 2023

* [X] Finish Pandas refactoring to all pipelines.
* [ ] refactor with data batches
* [ ] refactor the check with parallel read-only checks

We have refactored the pipelines to use Pandas.

Here are Feature Engineering results for `testing`:

```shell
(phdtrack-311) [onyr@kenzael feature_engineering]$ python main.py -p univariate_fs -o testing
🚀 Running program...
Passed program params:
param[0]: main.py
param[1]: -p
param[2]: univariate_fs
param[3]: -o
param[4]: testing
Program paths are OK.
2023-05-15 14:54:16,280 - results_logger - INFO - Program params:   [see below]
2023-05-15 14:54:16,280 - results_logger - INFO -       debug: False
2023-05-15 14:54:16,280 - results_logger - INFO -       max_ml_workers: 10
2023-05-15 14:54:16,281 - results_logger - INFO - timer for load_samples_and_labels_from_all_csv_files started
[...]
2023-05-15 14:54:17,127 - common_logger - INFO - Number of empty files: 0
2023-05-15 14:54:17,209 - results_logger - INFO - Time elapsed since the begining of load_samples_and_labels_from_all_csv_files: 0.9276196956634521 s
2023-05-15 14:54:17,211 - results_logger - INFO - Loaded data (performance_test)
2023-05-15 14:54:17,211 - results_logger - INFO - Number of positive labels: 7881
2023-05-15 14:54:17,211 - results_logger - INFO - Number of negative labels: 6268808
2023-05-15 14:54:17,429 - results_logger - INFO - Removing 1 columns with only one unique value: ['f_dtns_ancestor_1']
2023-05-15 14:54:17,514 - common_logger - INFO - Running pipeline: univariate_fs
2023-05-15 14:54:17,514 - results_logger - INFO - timer for pipeline (univariate_fs) started
2023-05-15 14:54:18,347 - common_logger - INFO - Column: f_dtn_byte_size, F-value: 2087.3490809533123, P-value: 0.0
2023-05-15 14:54:18,347 - common_logger - INFO - Column: f_position_in_dtn, F-value: 3053.101331057696, P-value: 0.0
2023-05-15 14:54:18,347 - common_logger - INFO - Column: f_dtn_ptrs, F-value: 362.21581144152526, P-value: 9.319301566180423e-81
2023-05-15 14:54:18,347 - common_logger - INFO - Column: f_dtn_vns, F-value: 3059.2963390076234, P-value: 0.0
2023-05-15 14:54:18,347 - common_logger - INFO - Column: f_ptrs_ancestor_1, F-value: 2716.8952251322835, P-value: 0.0
2023-05-15 14:54:18,347 - common_logger - INFO - Column: f_dtns_ancestor_2, F-value: 22312.312160777998, P-value: 0.0
2023-05-15 14:54:18,347 - common_logger - INFO - Column: f_ptrs_ancestor_2, F-value: 16160.007532569005, P-value: 0.0
2023-05-15 14:54:18,347 - common_logger - INFO - Column: f_dtns_ancestor_3, F-value: 17141.16951048605, P-value: 0.0
2023-05-15 14:54:18,347 - common_logger - INFO - Column: f_ptrs_ancestor_3, F-value: 86.7881934546351, P-value: 1.2082554110966134e-20
2023-05-15 14:54:18,347 - common_logger - INFO - Column: f_dtns_ancestor_4, F-value: 83.50892049684637, P-value: 6.344714376834052e-20
2023-05-15 14:54:18,347 - common_logger - INFO - Column: f_ptrs_ancestor_4, F-value: 52253.07861465121, P-value: 0.0
2023-05-15 14:54:18,347 - common_logger - INFO - Column: f_dtns_ancestor_5, F-value: 54386.05694874132, P-value: 0.0
2023-05-15 14:54:18,347 - common_logger - INFO - Column: f_ptrs_ancestor_5, F-value: 1795.3977717548285, P-value: 0.0
2023-05-15 14:54:18,347 - common_logger - INFO - Column: f_dtns_ancestor_6, F-value: 1798.7599774524347, P-value: 0.0
2023-05-15 14:54:18,347 - common_logger - INFO - Column: f_ptrs_ancestor_6, F-value: 65.88220380174491, P-value: 4.787797571504748e-16
2023-05-15 14:54:18,347 - common_logger - INFO - Column: f_dtns_ancestor_7, F-value: 65.30739322961306, P-value: 6.409170656923528e-16
2023-05-15 14:54:18,347 - common_logger - INFO - Column: f_ptrs_ancestor_7, F-value: 18373.698431339006, P-value: 0.0
2023-05-15 14:54:18,347 - results_logger - INFO - Column names sorted by importance: [f_dtns_ancestor_5, f_ptrs_ancestor_4, f_dtns_ancestor_2, f_ptrs_ancestor_7, f_dtns_ancestor_3, f_ptrs_ancestor_2, f_dtn_vns, f_position_in_dtn, f_ptrs_ancestor_1, f_dtn_byte_size, f_dtns_ancestor_6, f_ptrs_ancestor_5, f_dtn_ptrs, f_ptrs_ancestor_3, f_dtns_ancestor_4, f_ptrs_ancestor_6, f_dtns_ancestor_7]
2023-05-15 14:54:18,348 - results_logger - INFO - Time elapsed since the begining of pipeline (univariate_fs): 0.8337697982788086 s
```

With this, we can see that the most useful feature is `f_dtns_ancestor_5`. When we look at a sample file like `Performance_Test__chunck_idx-0_samples.csv`, we see that, searching for positive label lines (`,1\n`), we have a `1` value on this column. However, this is not the case for sample file `src/mem_to_graph/data/samples_and_labels/Performance_Test__chunck_idx-8_samples.csv`. This proably needs to be investigated

* [ ] Investigate the feature generation for column `f_dtns_ancestor_5` which is 0 for some sample files, and not for others.

##### working on training and evaluation: logistic regression

Now, we want to train and test a first simple ML model.

Logistic Regression is a Machine Learning algorithm that is used for binary classification problems (either 0 or 1). It's a statistical model that uses a logistic function to model a binary dependent variable. In other words, it predicts the probability of occurrence of an event by fitting data to a logistic function. Hence, it is also known as logistic regression. Since its outcome is discrete, it can be considered a statistical classification method.

The logistic function, also called the sigmoid function, can take any real-valued number and map it into a value between 0 and 1. If the curve goes to positive infinity, y predicted will become 1, and if the curve goes to negative infinity, y predicted will become 0. If the output of the sigmoid function is more than 0.5, we can classify the outcome as 1 or YES, and if it is less than 0.5, we can classify it as 0 or NO.

The reasons for choosing Logistic Regression in the given context are:

1. **Simplicity** : Logistic regression is straightforward to understand and explain, and can be regularized to avoid overfitting. Logistic models can be updated easily with new data using stochastic gradient descent.
2. **Binary Outcomes** : In the case where we are predicting two possible outcomes, logistic regression is a good starting algorithm to use.
3. **Probabilistic Approach** : Logistic regression not only gives a measure of how relevant a predictor (co-variable) is (coefficients); logistic regression also gives you the probability of the outcome when you plug in specific predictor values.
4. **Computational efficiency** : Logistic Regression is less computationally intensive compared to more complex models like neural networks, making it a good choice for problems that may not require the additional complexity.
5. **Baseline Model** : Logistic regression is a good baseline model to use for comparison with more complex algorithms. If a complex model is only slightly better than logistic regression, the computational cost may not be worth it, and logistic regression may be a better choice in that situation.

It's important to note that Logistic Regression assumptions include the independence of features, the linearity of features and log odds, and absence of missing values.

> We are not sure that our samples and labels are correct or complete, since it depends on JSON annotations. We have already seen a lot of missing values on the annotation files.

We have tried to use the logistic regression model with little success. This is probably due to the dataset being so imbalanced.

```shell
/home/onyr/anaconda3/envs/phdtrack-311/lib/python3.11/site-packages/sklearn/linear_model/_logistic.py:458: ConvergenceWarning: lbfgs failed to converge (status=1):
STOP: TOTAL NO. of ITERATIONS REACHED LIMIT.
```

##### random forest with undersampling

Since we have an imbalanced dataset, and since we have more a patern recognition problem that a statistical problem, a better idea is to use a **random forest classifier**.

Here are the results on the `testing` dataset.

```shell
(phdtrack-311) [onyr@kenzael feature_engineering]$ python main.py -p ml_random_forest -o testing
🚀 Running program...
Passed program params:
param[0]: main.py
param[1]: -p
param[2]: ml_random_forest
param[3]: -o
param[4]: testing
Program paths are OK.
2023-05-15 16:05:35,829 - results_logger - INFO - Program params:   [see below]
2023-05-15 16:05:35,829 - results_logger - INFO -       debug: False
2023-05-15 16:05:35,830 - results_logger - INFO -       max_ml_workers: 10
2023-05-15 16:05:35,831 - results_logger - INFO - timer for load_samples_and_labels_from_all_csv_files started
[...]
2023-05-15 16:05:36,559 - common_logger - INFO - Number of empty files: 0
2023-05-15 16:05:36,634 - results_logger - INFO - Time elapsed since the begining of load_samples_and_labels_from_all_csv_files: 0.8027958869934082 s
2023-05-15 16:05:36,636 - results_logger - INFO - Loaded data (performance_test)
2023-05-15 16:05:36,636 - results_logger - INFO - Number of positive labels: 7881
2023-05-15 16:05:36,636 - results_logger - INFO - Number of negative labels: 6268808
2023-05-15 16:05:36,846 - results_logger - INFO - Removing 1 columns with only one unique value: ['f_dtns_ancestor_1']
2023-05-15 16:05:36,918 - common_logger - INFO - Running pipeline: ml_random_forest
2023-05-15 16:05:36,919 - results_logger - INFO - timer for pipeline (ml_random_forest) started
2023-05-15 16:05:42,877 - common_logger - INFO - Precision: 0.12691517927657558, Recall: 0.9993781094527363, F1-score: 0.2252277505255781
2023-05-15 16:05:42,879 - results_logger - INFO - Time elapsed since the begining of pipeline (ml_random_forest): 5.960377216339111 s
```

We have a very bad precision but very good recall. This means that we retreive almost all keys, but most of what the model label as keys are actually not. As we try to maximize recall first, this is an interesting first result.