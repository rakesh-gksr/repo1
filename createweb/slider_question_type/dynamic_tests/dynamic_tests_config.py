# used the parametrized for advanced branching test cases. This test suite adds show and hide slider question
# Advanced Branching rule and verify test work as expected in preview and test window.
slider_qtype_predicates = [

    {
        'predicate_label': 'Predicate "contains all of" with "hide question" action',
        'branching_rule': [("MultipleChoice", [1, 1], "isoneof", ["Luka"], "hideq", "question", 2)],
        'rule_params': {'qType': 'multiChoice',
                        'qNum': 1,
                        'inputList': [1, 2],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"}
    },
    {
        'predicate_label': 'Predicate "contains all of" with "show question" action',
        'branching_rule': [("MultipleChoice", [1, 1], "isoneof", ["Luka"], "showq", "question", 2)],
        'rule_params': {'qType': 'multiChoice',
                        'qNum': 1,
                        'inputList': [1, 2],
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},
    }
    ]

# Manually created survey for slider question
survey_dict = {

    'MT1': {
        'slider_qtype_adv_branch': {
            'survey_id': '130985643', 'user_id': '61009464'},
        'slider_qtype_copy_transfer_survey': {
            "survey_id": "131054499",
            "user_id": "57534081",
            "title": "Survey_With_Slider_Ques",
            "slider_qtn_title":"acdVrixMZykSIkneUsuWclruOtSxQC"
        },
        'single_page_mode_copy_slider_question': {
            "survey_id": "132734740",
            "user_id": "61124194"
        },
        'survey_with_249_slider_question': {
            "survey_id": "131094413",
            "user_id": "57534081"
        }
    },
    'MT2': {
        'slider_qtype_adv_branch': {
            'survey_id': '130985643', 'user_id': '61009464'},
        'slider_qtype_copy_transfer_survey': {
            "survey_id": "131054499",
            "user_id": "57534081",
            "title": "Survey_With_Slider_Ques",
            "slider_qtn_title":"acdVrixMZykSIkneUsuWclruOtSxQC"
        },
        'single_page_mode_copy_slider_question': {
            "survey_id": "131094295",
            "user_id": "57534081"
        },
        'survey_with_249_slider_question': {
            "survey_id": "131094413",
            "user_id": "57534081"
        }
    },
    'MT3': {
        'slider_qtype_adv_branch': {
            'survey_id': '107138827', 'user_id': '87016048'},
        'slider_qtype_copy_transfer_survey': {
            "survey_id": "107138770",
            "user_id": "87016048",
            "title": "Survey_With_Slider_Ques",
            "slider_qtn_title":"acdVrixMZykSIkneUsuWclruOtSxQC"
        }
    },
    'MT4': {
        'slider_qtype_adv_branch': {
            'survey_id': '130985643', 'user_id': '61009464'},
        'slider_qtype_copy_transfer_survey': {
            "survey_id": "131054499",
            "user_id": "57534081",
            "title": "Survey_With_Slider_Ques",
            "slider_qtn_title": "acdVrixMZykSIkneUsuWclruOtSxQC"
        },
        'single_page_mode_copy_slider_question': {
            "survey_id": "132734740",
            "user_id": "61124194"
        },
        'survey_with_249_slider_question': {
            "survey_id": "131094413",
            "user_id": "57534081"
        }
    },
}
# answer dictionary for taking the survey with slider question
answers = {
    1: {
        1: {'input_text': '40'},
        2: {'input_text': '60'},
    }
}

