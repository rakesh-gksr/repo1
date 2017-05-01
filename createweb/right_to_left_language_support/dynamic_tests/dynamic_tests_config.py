# Test Data for parametrized test cases for RTL cases -
# https://sm01.testrail.net/index.php?/suites/view/47&group_by=cases:section_id&group_id=666795&group_order=asc

test_data_for_RTL_buttons_verification_after_switching_lang = [

    dict(language="Arabic",
         test_rail_id="C7133051",
         test_case_title="Verify creating couple of questions with rtl direction with survey language as Arabic. "
                         "After that switch to language like English and make sure on the saved fields with "
                         "rtl direction an ltr button is displayed to change the direction)"
         ),

    dict(language="Hebrew",
         test_rail_id="C21775200",
         test_case_title="Verify that ltr and rtl buttons appear only when survey language is hebrew(both in "
                         "inline and in advanced editor)"),

    dict(language="Persian",
         test_rail_id="C21775201",
         test_case_title="Verify creating couple of questions with rtl direction with survey language as Persian. "
                         "After that switch to language like English and make sure on the saved fields with "
                         "rtl direction an ltr button is displayed to change the direction"
         ),
]

test_data_for_verifying_saved_rtl_direction = [

    dict(language="Arabic",
         test_rail_id="C7133049",
         test_case_title="Verify you can change the direction and save using both rtl as well as ltr buttons."
         ),

    dict(language="Hebrew",
         test_rail_id="C21160227",
         test_case_title="Verify that ltr and rtl buttons appear only when survey language is hebrew(both in "
                         "inline and in advanced editor)"),

    dict(language="Persian",
         test_rail_id="C21160228",
         test_case_title="Verify that ltr and rtl buttons appear only when survey language is persian(both in "
                         "inline and in advanced editor)"
         ),
 ]

test_data_for_RTL_buttons_verification = [

    dict(language="Arabic",
         test_rail_id="C7133046",
         test_case_title="Verify that ltr and rtl buttons appear only when survey language is arabic (both in "
                         "inline and in advanced editor)"
         ),

    dict(language="Hebrew",
         test_rail_id="C19760467",
         test_case_title="Verify that ltr and rtl buttons appear only when survey language is hebrew(both in "
                         "inline and in advanced editor)"),

    dict(language="Persian",
         test_rail_id="C19760468",
         test_case_title="Verify that ltr and rtl buttons appear only when survey language is persian(both in "
                         "inline and in advanced editor)"
         ),
]

test_data_for_RTL_text_direction = [

    dict(language="Arabic",
         test_rail_id="C7133048 - C16892848",
         test_case_title="Verify that for a new edit question title/answer option, etc the default language is "
                         "rtl for the above mentioned languages."
         ),

    dict(language="Hebrew",
         test_rail_id="C19980458 - C23471854",
         test_case_title="Verify that ltr and rtl buttons appear only when survey language is hebrew(both in "
                         "inline and in advanced editor)"),

    dict(language="Persian",
         test_rail_id="C19980459 - C23471855",
         test_case_title="Verify that ltr and rtl buttons appear only when survey language is persian(both in "
                         "inline and in advanced editor)"
         ),
 ]

input_data_for_RTL_text_direction = [

    dict(input_type="String",
         question_title="Please classify the following Ships",
         answer_choice_title="Haruna"
         ),
    dict(input_type="Number",
         question_title="5244544534534",
         answer_choice_title="53453"
         ),
 ]

test_data_for_placeholder_verification = [

    dict(language="Arabic",
         test_rail_id="C16892850",
         test_case_title="Verify the placeholder text getting removed for the input fields as soon as the text is "
                         "typed in the field (Arabic)."
         ),
    dict(language="Hebrew",
         test_rail_id="C23677687",
         test_case_title="Verify the placeholder text getting removed for the input fields as soon as the text is "
                         "typed in the field (Hebrew)."
         ),
    dict(language="Persian",
         test_rail_id="C23677688",
         test_case_title="Verify the placeholder text getting removed for the input fields as soon as the text is "
                         "typed in the field (Persian)."
         ),
 ]
