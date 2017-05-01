input_data_for_score_validation = [

    dict(
        test_case_title="Verify the Score values does not accept non numeric characters",
        test_rail_id="C12809386",
        test_step_title="non numeric characters",
        score="@#$NJN",

         ),
    dict(
        test_case_title="Verify the Value does not accept negative numbers",
        test_rail_id="C12809387",
        test_step_title="negative numbers",
        score="-100"
    ),
 ]
