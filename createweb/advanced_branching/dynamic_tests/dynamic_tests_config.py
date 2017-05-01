# used the parametrized the page move related test cases
page_move_test_info = [
    {
        'jira_id': 'CREATE-6098',
        'test_case_title': "Moving page doesn't work with adv branching logic applied",
        'params': {'pFrom': 1, 'pTo': 2, 'position': 'after'},
        'branching_rule': [("MultipleChoice", [1, 1], "equals", [None], "finish", "default", None)],
        'page_move_step_title': "Move Page 1 after Page 2",
        'page_move_step_desc': "Verifies that Page 1 moved after Page 2.",
        'advance_branching_off': False

    },
    {
        'jira_id': 'CREATE-4949',
        'test_case_title': "Branching Action doesn't update on builder mode correctly when moving skip logic "
                           "destination page above page which has condition",
        'params': {'pFrom': 2, 'pTo': 1, 'position': 'before'},
        'branching_rule': [("MultipleChoice", [1, 1], "equals", [None], "skip", "default", 2)],
        'page_move_step_title': "Move Page 2 before Page 1",
        'page_move_step_desc': "Verifies that Page 2 moved before Page 1.",
        'advance_branching_off': True

    },
    {
        'jira_id': 'CREATE-6114',
        'test_case_title': "Advanced branching: moving page action menu isn't getting updated with page number",
        'params': {'pFrom': 1, 'pTo': 2, 'position': 'after'},
        'branching_rule': [("MultipleChoice", [1, 1], "equals", [None], "skip", "default", 2)],
        'page_move_step_title': "Move Page 1 after Page 2",
        'page_move_step_desc': "Verifies that Page 1 moved after Page 2.",
        'advance_branching_off': True

    },
]


# used the parametrized the advanced branching test cases. This test suite adds different different advanced
# branching rules and verify that they works as expected in Preview & Test.
adv_branch_test_info = [
    {
        'test_case_title': "Test adding other branching action hide question",
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["Cruise Ship"],
                        'logicType': 'page_skip',
                        'logicOptions':'Page 3'},

        'branching_rule': [("text", [1, 1], "contains", ["Ship"], "hideq", "question", 2)],
        'verify_advBranch_step_title': "Verify Advanced Branching - Hide Question Option under Other Actions",
        'verify_advBranch_step_desc': "verifies advanced branching - hide question option under other actions.",
        "error_message":'Failed to verify advanced branching - Hide Question option'


    },
    {
        'test_case_title': "Test adding other branching action show question",
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["Cruise Ship"],
                        'logicType': 'page_skip',
                        'logicOptions':'Page 2'},

        'branching_rule': [("text", [1, 1], "contains", ["Ship"], "showq", "question", 2)],
        'verify_advBranch_step_title': "Verify Advanced Branching - Show Question Option under Other Actions",
        'verify_advBranch_step_desc': "verifies advanced branching - show question option under other actions.",
        "error_message":'Failed to verify advanced branching - Hide Question option'

    },
    {
        'test_case_title': "Test adding branching condition 'AND'",
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["Cruise Ship"],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},

        'branching_rule': [("text", [1, 1], "equals", ["Cruise Ship"], "finish", "default", None, "and"),
                           ("text", [1, 1], "notequals", ["Ship"], "finish", "default", None)],
        'verify_advBranch_step_title': "Verify Advanced Branching AND Condition is Applied",
        'verify_advBranch_step_desc': "verifies advanced branching and condition is applied.",
        "error_message": 'Failed to verify advanced branching and condition is applied'
    },

    {
        'test_case_title': "Test adding branching condition 'OR'. \n Test adding branching action End Survey.",
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["Cruise Ship"],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},

        'branching_rule': [("text", [1, 1], "equals", ["Cruise Ship"], "finish", "default", None, "or"),
                           ("text", [1, 1], "equals", ["Ship"], "finish", "default", None)],
        'verify_advBranch_step_title': "Verify Advanced Branching OR Condition is Applied",
        'verify_advBranch_step_desc': "verifies advanced branching or condition is applied.",
        "error_message": 'Failed to verify advanced branching or condition is applied'
    },
    {
        'test_case_title': "Test adding branching action Disqualify respondent ",
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["Cruise Ship"],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},

        'branching_rule': [("text", [1, 1], "equals", ["Cruise Ship"], "disqualify", "default", None)],
        'verify_advBranch_step_title': "Verify Advanced Branching Disqualify Action",
        'verify_advBranch_step_desc': "verifies advanced branching disqualify action.",
        "error_message": 'Failed to verify advanced branching disqualify action'
    },


]

# used the parametrized for advanced branching test cases. This test suite adds AdvanceBranching to Transfered Survey
# from another user account.

adv_branch_transfer_survey = {
    'MT1': [
    {
        'AdvanceBranching': "On",
        'original_user_id': "58355061",
        'tranfer_survey_id': "130747967",
        'verify_advBranch_step_title': "Verify Advanced Branching is Applied",
        'verify_advBranch_step_desc': "verifies Advanced Branching is applied.",
        "error_message":'Failed to verify advanced branching logic.'
    },
    {
        'AdvanceBranching': "Off",
        'original_user_id': "58355061",
        'tranfer_survey_id': "132320958",
        'verify_advBranch_step_title': "Verify Advanced Branching is not applied",
        'verify_advBranch_step_desc': "verifies Advanced Branching is not applied.",
        "error_message":'Failed to verify advanced branching advanced branching logic.'
    }
    ],
    'MT2': [
        {
            'AdvanceBranching': "On",
            'original_user_id': "58355061",
            'tranfer_survey_id': "130747967",
            'verify_advBranch_step_title': "Verify Advanced Branching is Applied",
            'verify_advBranch_step_desc': "verifies Advanced Branching is applied.",
            "error_message": 'Failed to verify advanced branching logic.'
        },
        {
            'AdvanceBranching': "Off",
            'original_user_id': "58355061",
            'tranfer_survey_id': "130747968",
            'verify_advBranch_step_title': "Verify Advanced Branching is not applied",
            'verify_advBranch_step_desc': "verifies Advanced Branching is not applied.",
            "error_message": 'Failed to verify advanced branching advanced branching logic.'
        }
    ],
    'MT4': [
    {
        'AdvanceBranching': "On",
        'original_user_id': "58355061",
        'tranfer_survey_id': "130747967",
        'verify_advBranch_step_title': "Verify Advanced Branching is Applied",
        'verify_advBranch_step_desc': "verifies Advanced Branching is applied.",
        "error_message":'Failed to verify advanced branching logic.'
    },
    {
        'AdvanceBranching': "Off",
        'original_user_id': "58355061",
        'tranfer_survey_id': "132320958",
        'verify_advBranch_step_title': "Verify Advanced Branching is not applied",
        'verify_advBranch_step_desc': "verifies Advanced Branching is not applied.",
        "error_message":'Failed to verify advanced branching advanced branching logic.'
    }
    ]
    }

# used the parametrized for advanced branching test cases. This test suite adds AdvanceBranching to Copied Survey
# from another user account.
adv_branch_copy_survey = {
    'MT1': [
        {
            'AdvanceBranching': "On",
            'original_user_id': "58434593",
            'copy_survey_id': "130752772",
            'survey_title': 'AdvanceBranching_On',
            'verify_advBranch_step_title': "Verify Advanced Branching is Applied",
            'verify_advBranch_step_desc': "verifies Advanced Branching is applied.",
            "error_message":'Failed to verify advanced branching logic.'
        },
        {
            'AdvanceBranching': "Off",
            'original_user_id': "58434593",
            'copy_survey_id': "130752773",
            'survey_title': "AdvanceBranching_Off",
            'verify_advBranch_step_title': "Verify Advanced Branching is not applied",
            'verify_advBranch_step_desc': "verifies Advanced Branching is not applied.",
            "error_message":'Failed to verify advanced branching advanced branching logic.'
        }
    ],

    'MT2': [
        {
            'AdvanceBranching': "On",
            'original_user_id': "58434593",
            'copy_survey_id': "130752772",
            'survey_title': 'AdvanceBranching_On',
            'verify_advBranch_step_title': "Verify Advanced Branching is Applied",
            'verify_advBranch_step_desc': "verifies Advanced Branching is applied.",
            "error_message": 'Failed to verify advanced branching logic.'
        },
        {
            'AdvanceBranching': "Off",
            'original_user_id': "58434593",
            'copy_survey_id': "130752773",
            'survey_title': "AdvanceBranching_Off",
            'verify_advBranch_step_title': "Verify Advanced Branching is not applied",
            'verify_advBranch_step_desc': "verifies Advanced Branching is not applied.",
            "error_message": 'Failed to verify advanced branching advanced branching logic.'
        }
    ],
    'MT4': [
        {
            'AdvanceBranching': "On",
            'original_user_id': "58434593",
            'copy_survey_id': "130752772",
            'survey_title': 'AdvanceBranching_On',
            'verify_advBranch_step_title': "Verify Advanced Branching is Applied",
            'verify_advBranch_step_desc': "verifies Advanced Branching is applied.",
            "error_message": 'Failed to verify advanced branching logic.'
        },
        {
            'AdvanceBranching': "Off",
            'original_user_id': "58434593",
            'copy_survey_id': "130752773",
            'survey_title': "AdvanceBranching_Off",
            'verify_advBranch_step_title': "Verify Advanced Branching is not applied",
            'verify_advBranch_step_desc': "verifies Advanced Branching is not applied.",
            "error_message": 'Failed to verify advanced branching advanced branching logic.'
        }
    ]
}

