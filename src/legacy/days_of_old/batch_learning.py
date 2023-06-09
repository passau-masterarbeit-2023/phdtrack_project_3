def __ml_sgd_pipeline_partial_fit(
        params: ProgramParams, 
        samples_and_labels_train: SamplesAndLabelsGenerator,
        samples_and_labels_test: Optional[SamplesAndLabelsGenerator],
    ) -> None:
    """
    Note that we need to consume the data generator for the testing part.
    """

    # Train a SGDClassifier
    clf = SGDClassifier(random_state=42)
    params.results_manager.set_result_for(
        PipelineNames.ML_SGD ,"model_name", "sgd"
    )
    X_test_all = pd.DataFrame()
    y_test_all = pd.Series()
    
    for samples_train, labels_train in samples_and_labels_train:

        if samples_and_labels_test is None:
            # Split into train and test sets
            X_train, X_test, y_train, y_test = train_test_split(samples_train, labels_train, test_size=0.2, random_state=42)
            X_test_all = pd.concat([X_test_all, X_test])
            y_test_all = pd.concat([y_test_all, y_test])
        else:
            X_train, y_train = samples_train, labels_train

        # Perform undersampling on the majority class
        rus = RandomUnderSampler(random_state=42)
        X_res, y_res = rus.fit_resample(X_train, y_train)

        # Here classes=[0, 1] as we are assuming binary classification
        clf.partial_fit(X_res, y_res, classes=[0, 1])

    if samples_and_labels_test is not None:
        X_test_all, y_test_all = consume_data_generator(samples_and_labels_test)

    # Make predictions on the test set
    y_pred = clf.predict(X_test_all)

    # Compute metrics
    precision = precision_score(y_test_all, y_pred)
    recall = recall_score(y_test_all, y_pred)
    f1 = f1_score(y_test_all, y_pred)

    # Log the results
    params.RESULTS_LOGGER.info(f'Precision: {precision}, Recall: {recall}, F1-score: {f1}')
