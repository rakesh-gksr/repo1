# Following list used to parametrized the Multiple Choice Multiple Answer question type test cases for its different
#  predicates.
multiple_choice_multiple_answer_predicates = [

    {

        'predicate_label': 'Predicate "not contains any of" with "show question" action',
        'branching_rule': [("MultipleChoice", [1, 1], "notcontainsanyof", ["A", "A"], "showq", "question", 2)],
        'rule_params': {'qType': 'multiChoice',
                        'qNum': 1,
                        'inputList': [2],
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},

    },
    {

        'predicate_label': 'Predicate "contains any of" with "hideq" action',
        'branching_rule': [("MultipleChoice", [1, 1], "containsanyof", ["B"], "hideq", "question", 2)],
        'rule_params': {'qType': 'multiChoice',
                        'qNum': 1,
                        'inputList': [1, 2],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},

    },
    {

        'predicate_label': 'Predicate "not contains" with "disqualify" action',
        'branching_rule': [("MultipleChoice", [1, 1], "notcontains", ["A"], "disqualify", "default", None)],
        'rule_params': {'qType': 'multiChoice',
                        'qNum': 1,
                        'inputList': [2],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},

    },
    {
        'predicate_label': 'Predicate "contains" with "hide page" action',
        'branching_rule': [("MultipleChoice", [1, 1], "contains", ["A','A"], "hidep", "default", 2)],
        'rule_params': {'qType': 'multiChoice',
                        'qNum': 1,
                        'inputList': [1],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},

    },
    {
        'predicate_label': 'Predicate "no response" with "page skip" action',
        'branching_rule': [("MultipleChoice", [1, 1], "noresponse", [None], "skip", "default", 2)],
        'rule_params': {'qType': 'multiChoice',
                        'qNum': 1,
                        'inputList': None,
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},

    },
    {
        'predicate_label': 'Predicate "has a response" with "end survey" action',
        'branching_rule': [("MultipleChoice", [1, 1], "response", [None], "showp", "default", 2)],
        'rule_params': {'qType': 'multiChoice',
                        'qNum': 1,
                        'inputList': [1],
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},

    },
    {
        'predicate_label': 'Predicate "not equals" with "finish" action',
        'branching_rule': [("MultipleChoice", [1, 1], "notequals", ["A"], "finish", "default", None)],
        'rule_params': {'qType': 'multiChoice',
                        'qNum': 1,
                        'inputList': [2],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"}
    },
    {
        'predicate_label': 'Predicate "equals" with "finish" action',
        'branching_rule': [("MultipleChoice", [1, 1], "equals", [None], "finish", "default", None)],
        'rule_params': {'qType': 'multiChoice',
                        'qNum': 1,
                        'inputList': [1],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"}
    },
    {
        'predicate_label': 'Predicate "not contains all of" with "hide page" action',
        'branching_rule': [("MultipleChoice", [1, 1], "notcontainsallof", [None], "hidep", "default", 2)],
        'rule_params': {'qType': 'multiChoice',
                        'qNum': 1,
                        'inputList': [2],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"}
    },
    {
        'predicate_label': 'Predicate "contains all of" with "finish" action',
        'branching_rule': [("MultipleChoice", [1, 1], "containsallof", ["B"], "finish", "default", None)],
        'rule_params': {'qType': 'multiChoice',
                        'qNum': 1,
                        'inputList': [1, 2],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"}
    },
    {
        'predicate_label': 'Predicate "contains all of" with "hide quesiton" action',
        'branching_rule': [("MultipleChoice", [1, 1], "containsallof", ["B"], "hideq", "question", 2)],
        'rule_params': {'qType': 'multiChoice',
                        'qNum': 1,
                        'inputList': [1, 2],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"}
    }

]

# Following list used to parametrized the Multiple Choice question type test cases for its different
#  predicates.
multiple_choice_predicates = [


    {
        'predicate_label': 'Predicate "is not any of" with "hide question" action',
        'branching_rule': [("MultipleChoice", [1, 1], "notisoneof", [None], "hideq", "question", 2)],
        'rule_params': {'qType': 'multiChoice',
                        'qNum': 1,
                        'inputList': [2],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},

    },
    {
        'predicate_label': 'Predicate "is one of" with "disqualify" action',
        'branching_rule': [("MultipleChoice", [1, 1], "isoneof", ["A", "A"], "disqualify", "default", None)],
        'rule_params': {'qType': 'multiChoice',
                        'qNum': 1,
                        'inputList': [1],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},
    },

    {
        'predicate_label': 'Predicate "no response" with "page skip" action',
        'branching_rule': [("MultipleChoice", [1, 1], "noresponse", [None], "skip", "default", 2)],
        'rule_params': {'qType': 'multiChoice',
                        'qNum': 1,
                        'inputList': None,
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},

    },
    {
        'predicate_label': 'Predicate "has a response" with "hide page" action',
        'branching_rule': [("MultipleChoice", [1, 1], "response", [None], "hidep", "default", 2)],
        'rule_params': {'qType': 'multiChoice',
                        'qNum': 1,
                        'inputList': [1],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},

    },
    {
        'predicate_label': 'Predicate "not equals" with "show page" action',
        'branching_rule': [("MultipleChoice", [1, 1], "notequals", ["A"], "showp", "default", 2)],
        'rule_params': {'qType': 'multiChoice',
                        'qNum': 1,
                        'inputList': [2],
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},
    },
    {
        'predicate_label': 'Predicate "equals" with "finish" action',
        'branching_rule': [("MultipleChoice", [1, 1], "equals", [None], "finish", "default", None)],
        'rule_params': {'qType': 'multiChoice',
                        'qNum': 1,
                        'inputList': [1],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"}
    }
]

# Following list used to parametrized the Dropdown question type test cases for its different
#  predicates.
dropdown_qtype_predicates = [
    {
        'predicate_label': 'Predicate "is not any of" with "hide question" action',
        'branching_rule': [("MultipleChoice", [1, 1], "notisoneof", [None], "hideq", "question", 2)],
        'rule_params': {'qType': 'dropdown',
                        'qNum': 1,
                        'inputList': ["B"],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},

    },
    {
        'predicate_label': 'Predicate "is one of" with "disqualify" action',
        'branching_rule': [("MultipleChoice", [1, 1], "isoneof", ["A", "A"], "disqualify", "default", None)],
        'rule_params': {'qType': 'dropdown',
                        'qNum': 1,
                        'inputList': ["A"],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},
    },

    {
        'predicate_label': 'Predicate "no response" with "page skip" action',
        'branching_rule': [("MultipleChoice", [1, 1], "noresponse", [None], "skip", "default", 2)],
        'rule_params': {'qType': 'dropdown',
                        'qNum': 1,
                        'inputList': None,
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},

    },
    {
        'predicate_label': 'Predicate "has a response" with "hide page" action',
        'branching_rule': [("MultipleChoice", [1, 1], "response", [None], "hidep", "default", 2)],
        'rule_params': {'qType': 'dropdown',
                        'qNum': 1,
                        'inputList': ["A"],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},

    },
    {
        'predicate_label': 'Predicate "not equals" with "show page" action',
        'branching_rule': [("MultipleChoice", [1, 1], "notequals", ["A"], "showp", "default", 2)],
        'rule_params': {'qType': 'dropdown',
                        'qNum': 1,
                        'inputList': ["B"],
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},
    },
    {
        'predicate_label': 'Predicate "equals" with "finish" action',
        'branching_rule': [("MultipleChoice", [1, 1], "equals", [None], "finish", "default", None)],
        'rule_params': {'qType': 'dropdown',
                        'qNum': 1,
                        'inputList': ["A"],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"}
    }
]
# Following list used to parametrized the test cases for each predicates of following question types
# 1. Matrix Rating Scale question type
# 2. Matrix Rating Scale Single row rating scale question type
# 3. Matrix Rating Scale with weights question type
# 4. Matrix Rating Scale non weights question type

matrix_rating_scal_qtype_predicates = [
    {
        'predicate_label': 'Predicate "is not any of" with "hide question" action',
        'branching_rule': [("matrix", [1, 1, 1], "notisoneof", [None], "hideq", "question", 2)],
        'rule_params': {'qType': 'matrix',
                        'qNum': 1,
                        'inputList': [(1, 2)],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},

    },
    {
        'predicate_label': 'Predicate "is one of" with "disqualify" action',
        'branching_rule': [("matrix", [1, 1, 1], "isoneof", ["Light Cruiser(CL)"], "disqualify", "default", None)],
        'rule_params': {'qType': 'matrix',
                        'qNum': 1,
                        'inputList': [(1, 1),(1, 2)],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},
    },
    {
        'predicate_label': 'Predicate "no response" with "page skip" action',
        'branching_rule': [("matrix", [1, 1, 1], "noresponse", [None], "skip", "default", 2)],
        'rule_params': {'qType': 'matrix',
                        'qNum': 1,
                        'inputList': None,
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},

    },
    {
        'predicate_label': 'Predicate "has a response" with "hide page" action',
        'branching_rule': [("matrix", [1, 1, 1], "response", [None], "hidep", "default", 2)],
        'rule_params': {'qType': 'matrix',
                        'qNum': 1,
                        'inputList': [(1, 1)],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},

    },
    {
        'predicate_label': 'Predicate "not equals" with "show page" action',
        'branching_rule': [("matrix", [1, 1, 1], "notequals", ["Aircraft Carrier(CV)"], "showp", "default", 2)],
        'rule_params': {'qType': 'matrix',
                        'qNum': 1,
                        'inputList': [(1, 2)],
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},
    },
    {
        'predicate_label': 'Predicate "equals" with "finish" action',
        'branching_rule': [("matrix", [1, 1, 1], "equals", ["Battleship(BB)"], "finish", "default", None)],
        'rule_params': {'qType': 'matrix',
                        'qNum': 1,
                        'inputList': [(1, 3)],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"}
    }
]

matrix_of_dropdown_menus_predicates = [
    {
        'predicate_label': 'Predicate "is not any of" with "hide question" action',
        'branching_rule': [("menuMatrix", [1, 1, 1, 1], "notisoneof", [None], "hideq", "question", 2)],
        'rule_params': {'qType': 'menuMatrix',
                        'qNum': 1,
                        'inputList': [(1, 1, 2)],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},

    },
    {
        'predicate_label': 'Predicate "is one of" with "disqualify" action',
        'branching_rule': [("menuMatrix", [1, 1, 1, 1], "isoneof", ["Yes','Yes"], "disqualify", "default", None)],
        'rule_params': {'qType': 'menuMatrix',
                        'qNum': 1,
                        'inputList': [(1, 1, 1)],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},
    },
    {
        'predicate_label': 'Predicate "no response" with "page skip" action',
        'branching_rule': [("menuMatrix", [1, 1, 2, 1], "noresponse", [None], "skip", "default", 2)],
        'rule_params': {'qType': 'menuMatrix',
                        'qNum': 1,
                        'inputList': None,
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},

    },
    {
        'predicate_label': 'Predicate "has a response" with "hide page" action',
        'branching_rule': [("menuMatrix", [1, 1, 1, 1], "response", [None], "hidep", "default", 2)],
        'rule_params': {'qType': 'menuMatrix',
                        'qNum': 1,
                        'inputList': [(1, 1, 1)],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},

    },
    {
        'predicate_label': 'Predicate "not equals" with "show page" action',
        'branching_rule': [("menuMatrix", [1, 1, 1, 1], "notequals", ["Yes", "No"], "showp", "default", 2)],
        'rule_params': {'qType': 'menuMatrix',
                        'qNum': 1,
                        'inputList': [(1, 1, 1)],
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},
    },
    {
        'predicate_label': 'Predicate "equals" with "finish" action',
        'branching_rule': [("menuMatrix", [1, 1, 1, 1], "equals", [None], "finish", "default", None)],
        'rule_params': {'qType': 'menuMatrix',
                        'qNum': 1,
                        'inputList': [(1, 1, 1)],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"}
    }
]

# Following list used to parametrized the ranking question type test cases for its different
#  predicates.
ranking_qtype_predicates = [
    {
        'predicate_label': 'Predicate "is not any of" with "hide question" action',
        'branching_rule': [("matrix", [1, 1, 1], "notisoneof", [None], "hideq", "question", 2)],
        'rule_params': {'qType': 'ranking',
                        'qNum': 1,
                        'inputList': [(1, 2)],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},

    },
    {
        'predicate_label': 'Predicate "is one of" with "disqualify" action',
        'branching_rule': [("matrix", [1, 1, 1], "isoneof", ["2"], "disqualify", "default", None)],
        'rule_params': {'qType': 'ranking',
                        'qNum': 1,
                        'inputList': [(1, 1)],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},
    },
    {
        'predicate_label': 'Predicate "no response" with "page skip" action',
        'branching_rule': [("matrix", [1, 1, 1], "noresponse", [None], "skip", "default", 2)],
        'rule_params': {'qType': 'ranking',
                        'qNum': 1,
                        'inputList': None,
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},

    },
    {
        'predicate_label': 'Predicate "has a response" with "hide page" action',
        'branching_rule': [("matrix", [1, 1, 1], "response", [None], "hidep", "default", 2)],
        'rule_params': {'qType': 'ranking',
                        'qNum': 1,
                        'inputList': [(1, 1)],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},

    },
    {
        'predicate_label': 'Predicate "not equals" with "show page" action',
        'branching_rule': [("matrix", [1, 1, 1], "notequals", [1], "showp", "default", 2)],
        'rule_params': {'qType': 'ranking',
                        'qNum': 1,
                        'inputList': [(1, 2)],
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},
    },
    {
        'predicate_label': 'Predicate "equals" with "finish" action',
        'branching_rule': [("matrix", [1, 1, 2], "equals", [1], "finish", "default", None)],
        'rule_params': {'qType': 'ranking',
                        'qNum': 1,
                        'inputList': [(2, 1)],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"}
    }

]


# Predicates for Single Textbox Question
single_textbox_predicates = [
    {
        'predicate_label': 'Predicate "has a response" with "hide question" action',
        'branching_rule': [("text", [1, 1], "response", [None], "hideq", "question", 2)],
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["Cruise Ship"],
                        'logicType': 'page_skip',
                        'logicOptions':"Page 3"},
    },
    {
        'predicate_label': 'Predicate "is not" with "Hide page" action',
        'branching_rule': [("text", [1, 1], "notequals", ["False"], "hidep", "default", 2)],
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["Cruise"],
                        'logicType': 'page_skip',
                        'logicOptions': "Page 3"},
    },
    {
        'predicate_label': 'Predicate "contains" with "show page" action',
        'branching_rule': [("text", [1, 1], "contains", ["Ship"], "showp", "default", 2)],
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["Cruise Ship"],
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},
    },
    {
        'predicate_label': 'Predicate "does not contains" with "show question" action',
        'branching_rule': [("text", [1, 1], "notcontains", ["Ship"], "showq", "question", 2)],
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["Cruise"],
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},
    },
    {
        'predicate_label': 'Predicate "starts with" with "disqualify" action',
        'branching_rule': [("text", [1, 1], "startswith", ["Cruise"], "disqualify", "default", None)],
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["Cruise Ship"],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},
    },
    {
        'predicate_label': 'Predicate "ends with" with "disqualify" action',
        'branching_rule': [("text", [1, 1], "endswith", ["Ship"], "disqualify", "default", None)],
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["Cruise Ship"],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},
    },
    {
        'predicate_label': 'Predicate "is exactly" with "invalidate" action',
        'branching_rule': [("text", [1, 1], "equals", ["Cruise Ship"], "invalidate", "question_error", [2, "INVALIDATED"])],
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["Cruise Ship"],
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},
    },
]


# Predicates for Multiple Textbox Question
multiple_textbox_predicates = [
    {
        'predicate_label': 'Predicate "has a response" with "hide question" action',
        'branching_rule': [("multibox", [1, 1, 1], "response", [None], "hideq", "question", 2)],
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["Cruise Ship"],
                        'logicType': 'page_skip',
                        'logicOptions':"Page 3"},
    },
    {
        'predicate_label': 'Predicate "is not" with "Hide page" action',
        'branching_rule': [("multibox", [1, 1, 1], "notequals", ["False"], "hidep", "default", 2)],
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["Cruise"],
                        'logicType': 'page_skip',
                        'logicOptions': "Page 3"},
    },
    {
        'predicate_label': 'Predicate "contains" with "show page" action',
        'branching_rule': [("multibox", [1, 1, 1], "contains", ["Ship"], "showp", "default", 2)],
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["Cruise Ship"],
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},
    },
    {
        'predicate_label': 'Predicate "does not contains" with "show question" action',
        'branching_rule': [("multibox", [1, 1, 1], "notcontains", ["Ship"], "showq", "question", 2)],
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["Cruise"],
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},
    },
    {
        'predicate_label': 'Predicate "starts with" with "disqualify" action',
        'branching_rule': [("multibox", [1, 1, 1], "startswith", ["Cruise"], "disqualify", "default", None)],
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["Cruise Ship"],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},
    },
    {
        'predicate_label': 'Predicate "ends with" with "disqualify" action',
        'branching_rule': [("multibox", [1, 1, 1], "endswith", ["Ship"], "disqualify", "default", None)],
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["Cruise Ship"],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},
    },
    {
        'predicate_label': 'Predicate "is exactly" with "invalidate" action',
        'branching_rule': [("multibox", [1, 1, 1], "equals", ["Cruise Ship"], "invalidate", "question_error", [2, "INVALIDATED"])],
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["Cruise Ship"],
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},
    },
]


# Predicates for multiple textboxes numeric type
multiple_textbox_numeric_predicates = [
    {
        'predicate_label': 'Predicate "has a response" with "hide question" action',
        'branching_rule': [("multibox", [1, 1, 1], "response", [None], "hideq", "question", 2)],
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["111"],
                        'logicType': 'page_skip',
                        'logicOptions':"Page 3"},
    },
    {
        'predicate_label': 'Predicate "is not" with "Hide page" action',
        'branching_rule': [("multibox", [1, 1, 1], "notequals", ["False"], "hidep", "default", 2)],
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["2323"],
                        'logicType': 'page_skip',
                        'logicOptions': "Page 3"},
    },
    {
        'predicate_label': 'Predicate "contains" with "show page" action',
        'branching_rule': [("multibox", [1, 1, 1], "contains", ["123"], "showp", "default", 2)],
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["1412356"],
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},
    },
    {
        'predicate_label': 'Predicate "does not contains" with "show question" action',
        'branching_rule': [("multibox", [1, 1, 1], "notcontains", ["543"], "showq", "question", 2)],
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["1222"],
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},
    },
    {
        'predicate_label': 'Predicate "starts with" with "disqualify" action',
        'branching_rule': [("multibox", [1, 1, 1], "startswith", ["45"], "disqualify", "default", None)],
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["4566667"],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},
    },
    {
        'predicate_label': 'Predicate "ends with" with "disqualify" action',
        'branching_rule': [("multibox", [1, 1, 1], "endswith", ["66"], "disqualify", "default", None)],
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["122266"],
                        'logicType': 'end_survey',
                        'logicOptions': "That's the end of the preview!"},
    },
    {
        'predicate_label': 'Predicate "is exactly" with "invalidate" action',
        'branching_rule': [("multibox", [1, 1, 1], "equals", ["0896"], "invalidate", "question_error", [2, "INVALIDATED"])],
        'rule_params': {'qType': 'text',
                        'qNum': 1,
                        'inputList': ["0896"],
                        'logicType': 'page_skip',
                        'logicOptions': "Page 2"},
    },
]

survey_dict= {

    'dropdown_qtype':{
        'survey_id': '130794880',
        'user_id': '58439685'},

    'matrix_menus_qtype': {
        'survey_id': '130801250',
        'user_id': '58439685'
},
    'matrix_rating_scale': {
        'survey_id': '130800680',
        'user_id': '58439685'
    },
    'matrix_rating_scale_with_no_weights': {
        'survey_id': '130800778',
        'user_id': '58439685'
    },
    'matrix_rating_scale_with_weights': {
        'survey_id': '130800706',
        'user_id': '58439685'
    },
    'multiple_choice_multi_answer': {
        'survey_id': '130783126',
        'user_id': '58434593'
    },
    'multiple_choice': {
        'survey_id': '130789031',
        'user_id': '58434593'
    },
    'numeric_multiple_textbox': {
        'survey_id': '130820335',
        'user_id': '58439685'
    },
    'multiple_textbox': {
        'survey_id': '130793381',
        'user_id': '58439685'
    },
    'ranking_qtype': {
        'survey_id': '130820371',
        'user_id': '61009464'
    },
    'single_textbox': {
        'survey_id': '130788901',
        'user_id': '58439685'
    }
}
