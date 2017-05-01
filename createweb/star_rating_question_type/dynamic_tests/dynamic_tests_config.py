# Manually created survey for star rating question
survey_dict = {

    'MT1': {
        'star_qtype_copy_transfer_survey': {
            "survey_id": "131153526",
            "user_id": "57534081",
            "title": "Survey_With_Star_Ques",
            "star_qtn_title": "acdVrixMZykSIkneUsuWclruOtSxQC"
        },
        'star_qtype_adv_branch': {
            'survey_id': '131203254', 'user_id': '57534081'},
    },
    'MT2': {
        'star_qtype_copy_transfer_survey': {
            "survey_id": "131153526",
            "user_id": "57534081",
            "title": "Survey_With_Star_Ques",
            "star_qtn_title": "acdVrixMZykSIkneUsuWclruOtSxQC"
        },
        'star_qtype_adv_branch': {
            'survey_id': '131203254', 'user_id': '57534081'},
    },
    'MT3': {
        'star_qtype_copy_transfer_survey': {
            "survey_id": "107333533",
            "user_id": "87016050",
            "title": "Survey_With_Star_Ques",
            "star_qtn_title": "acdVrixMZykSIkneUsuWclruOtSxQC"
        },
        'star_qtype_adv_branch': {
            'survey_id': '107333532', 'user_id': '87016050'},

        },
    'MT4': {
        'star_qtype_copy_transfer_survey': {
            "survey_id": "131153526",
            "user_id": "57534081",
            "title": "Survey_With_Star_Ques",
            "star_qtn_title": "acdVrixMZykSIkneUsuWclruOtSxQC"
        },
        'star_qtype_adv_branch': {
            'survey_id': '131203254', 'user_id': '57534081'},
    },
    }

# used the parametrized for advanced branching test cases. This test suite adds show and hide star question
# Advanced Branching rule and verify test work as expected in preview and test window.
star_qtype_predicates = [

    {
        'title': 'verify hiding star question on branching action condition',
        'testrail_id': 'C812401',
        'branching_rule': [("MultipleChoice", [1, 1], "isoneof", ["Luka"], "hideq", "question", 2)],
        'rule_params': {'qType': 'multiChoice',
                        'qNum': 1,
                        'inputList': [1, 2],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"}
    },
    {
        'title': 'verify showing star question on branching action condition',
        'testrail_id': 'C921898',
        'branching_rule': [("MultipleChoice", [1, 1], "isoneof", ["Luka"], "showq", "question", 2)],
        'rule_params': {'qType': 'multiChoice',
                        'qNum': 1,
                        'inputList': [1, 2],
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},
    }
    ]
