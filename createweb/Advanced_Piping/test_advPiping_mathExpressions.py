#!/usr/bin/env python
# -*- coding: utf-8 -*-

from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAdvPipingMathExpressions/",  # report_relative_location
                               "test_advPiping_mathExpressions",  # report_file_name_prefix
                               "Verify advance piping from Multiple Choice qtype with expressions",  # test_suite_title
                               ("This test adds Multiple Choice type question "
                                " and then verifies advanced piping to all question type except NPS."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os

    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime(
        "%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()

    request.addfinalizer(fin)
    return report, testcasename

expression_list = [
    dict(testcase="Basic Numbers",
         expression="3 + 5 * 12 - 8 / 4",
         expected_answer="61"),
    dict(testcase="Orders of Operation",
         expression="(3 + 5) * (12 - 8) / 4",
         expected_answer="8"),
    dict(testcase="Floating Point",
         expression="1.1 + 1.1 + 1.1",
         expected_answer="3.3"),
    dict(testcase="Equal",
         expression="3 = 5",
         expected_answer="FALSE"),
    dict(testcase="Less Than",
         expression="99 < 100",
         expected_answer="TRUE"),
    dict(testcase="Less Than Equal",
         expression="100 <= 100",
         expected_answer="TRUE"),
    dict(testcase="Greater Than Negative",
         expression="-5 > -3",
         expected_answer="FALSE"),
    dict(testcase="Standard String",
         expression=u"\"This is a string.\"",
         expected_answer="This is a string."),
    dict(testcase="Multi String",
         expression=u"\'The string above is: \"This is a string.\"\'",
         expected_answer="The string above is: \"This is a string.\""),
    dict(testcase="Multi Language String",
         expression=u"\"\\\"吾輩は猫である\\\" means \\\"I am a cat\\\" in Japanese.\"",
         expected_answer=u"\"吾輩は猫である\" means \"I am a cat\" in Japanese."),
    dict(testcase="Empty String",
         expression="\"\" + 0",
         expected_answer=""),
    dict(testcase="String to Int",
         expression="\"10\" + 0",
         expected_answer="10"),
    dict(testcase="US to Integer",
         expression="\"19.35\" + 0",
         expected_answer="19.35"),
    dict(testcase="Invalid trailing chars to Integer",
         expression="\"1.1,1.1\" + 0",
         expected_answer=""),
    dict(testcase="Greater Than Empty String",
         expression="\"\" > 5",
         expected_answer=""),
    dict(testcase="Less Than Equal String",
         expression="\"3\" <= 3.1",
         expected_answer="TRUE"),
    dict(testcase="Less Than String",
         expression="1000 < \"1530.35\"",
         expected_answer="TRUE"),
    dict(testcase="Lexicographic Ordering",
         expression="\"ab\" < \"ac\"",
         expected_answer="TRUE"),
    dict(testcase="Locale Unicode Lexicographic Ordering",
         expression=u"\"café\" < \"caffeine\"",
         expected_answer="TRUE"),
    dict(testcase="Canadian Locale Lexicographic Ordering",
         expression=u"\"coté\" < \"côte\"",
         expected_answer="FALSE"),
    dict(testcase="Null addition",
         expression="NULL + 3",
         expected_answer=""),
    dict(testcase="Null math",
         expression="1 + 3 * NULL - 5",
         expected_answer=""),
    dict(testcase="Divide by Zero",
         expression=" 1 / 0",
         expected_answer=""),
    dict(testcase="Null Comparison",
         expression="NULL >= 5",
         expected_answer=""),
    dict(testcase="Strict Equality Equals",
         expression=u"\"Résumé\" = \"résumé\"",
         expected_answer="FALSE"),
    dict(testcase="Strict Equality IS",
         expression=u"\"Résumé\" IS \"résumé\"",
         expected_answer="FALSE"),
    dict(testcase="Membership True",
         expression="3 IN [1, 2, 3]",
         expected_answer="TRUE"),
    dict(testcase="Membership False",
         expression="5 IN [1, 2]",
         expected_answer="FALSE"),
    dict(testcase="Containment 1",
         expression="\"this is a test\" ~ \"test\"",
         expected_answer="TRUE"),
    dict(testcase="Containment 2",
         expression="\"this is a test\" ~ \"^test\"",
         expected_answer="FALSE"),
    dict(testcase="Containment 3",
         expression="\"this is a test\" ~ \"^this\"",
         expected_answer="TRUE"),
    dict(testcase="Containment 4",
         expression="\"this is a test\" ~ \"te?t\"",
         expected_answer="FALSE"),
    dict(testcase="Containment 5",
         expression="\"this is a test\" ~ \"te*\"",
         expected_answer="FALSE"),
    dict(testcase="Unicode Containment 1",
         expression=u"\"RÉSUMÉ\" ~ \"resume\"",
         expected_answer="FALSE"),
    dict(testcase="Unicode Containment 2",
         expression=u"\"Résumé\" ~ \"résumé\"",
         expected_answer="TRUE"),
    dict(testcase="Unicode Containment 3",
         expression=u"\"resume\" ~ \"résumé\"",
         expected_answer="FALSE"),
    dict(testcase="Unicode Containment 4",
         expression=u"\"weißwurst\" ~ \"weiss\"",
         expected_answer="FALSE"),
    dict(testcase="Unicode Containment 5",
         expression=u"\"weisswurst\" ~ \"weiß\"",
         expected_answer="FALSE"),
    dict(testcase="Unicode Containment 6",
         expression=u"\"パス\" ~ \"ハス\"",
         expected_answer="FALSE"),
    dict(testcase="Unicode Containment 7",
         expression=u"\"バス\" ~ \"ハス\"",
         expected_answer="FALSE"),
    dict(testcase="Unicode Containment 8",
         expression=u"\"パス\" ~ \"バス\"",
         expected_answer="FALSE"),
    dict(testcase="Length Function",
         expression="LEN([1,2,3,4,5])",
         expected_answer="5"),
    dict(testcase="Length Function",
         expression="LEN([1,2,3,4,5])",
         expected_answer="5"),
    dict(testcase="MIN Function",
         expression="MIN(1,2,3,4,5)",
         expected_answer="1"),
    dict(testcase="MAX Function",
         expression="MAX(1,2,3,4,5)",
         expected_answer="5"),
    dict(testcase="SUM Function",
         expression="SUM(1,2,3,4,5)",
         expected_answer="15"),
    dict(testcase="AVG Function",
         expression="AVG(1,2,3,4,5)",
         expected_answer="3"),
    dict(testcase="STDEV Function",
         expression="STDEV(1,2,3,4,5)",
         expected_answer="1.58113883008"),
    dict(testcase="STDEVP Function",
         expression="STDEVP(1,2,3,4,5)",
         expected_answer="1.41421356237"),
    dict(testcase="IF Function",
         expression="IF(1=1, AVG(1,2,3), AVG(4,5,6))",
         expected_answer="2"),
    dict(testcase="CONCAT Function",
         expression="CONCAT(\"Yuudachi\",\"-\",\"poi\",\"!~\")",
         expected_answer="Yuudachi-poi!~"),
    dict(testcase="COALESCE Function",
         expression="COALESCE(NULL,1,2,3)",
         expected_answer="1"),
    dict(testcase="INT Function",
         expression="INT(\"42\")",
         expected_answer="42"),
    dict(testcase="BOOL Function",
         expression="BOOL(1=2)",
         expected_answer="FALSE"),
    dict(testcase="REAL Function",
         expression="REAL(\"3.1415\")",
         expected_answer="3.1415"),
    dict(testcase="STR Function",
         expression="STR(42)",
         expected_answer="42"),
    dict(testcase="PRECISION Function",
         expression="PRECISION(3.14159265359, 5)",
         expected_answer="3.14159"),
    dict(testcase="SUBSTR Function",
         expression="SUBSTR(\"poipoipoi\",3,6)",
         expected_answer="poipoi"),
    dict(testcase="TRIM Function",
         expression="TRIM(\"          poipoipoi         \")",
         expected_answer="poipoipoi"),
    dict(testcase="MOD Function",
         expression="MOD(3,2)",
         expected_answer="1"),
    dict(testcase="POW Function",
         expression="POW(2,2)",
         expected_answer="4"),
    dict(testcase="LCM Function",
         expression="LCM(9,12)",
         expected_answer="36"),
    dict(testcase="GCD Function",
         expression="GCD(8,12)",
         expected_answer="4"),
    dict(testcase="STRSPLIT Function",
         expression="STRSPLIT(\"IpoiAmpoiApoiStringpoi\",\"poi\")",
         expected_answer="I, Am, A, String,"),
    dict(testcase="STRJOIN Function",
         expression="STRJOIN(\"*\",[\"poi\",\"desu\",\"nanodesu\",\"khorosho\"])",
         expected_answer="poi*desu*nanodesu*khorosho"),
    dict(testcase="PART Function",
         expression="PART([0,1,2,3,4,5],5)",
         expected_answer="5"),
    dict(testcase="SGN Function",
         expression="SGN(-42)",
         expected_answer="-1"),
    dict(testcase="ABS Function",
         expression="ABS(-42)",
         expected_answer="42"),
    dict(testcase="FLOOR Function",
         expression="FLOOR(3.14)",
         expected_answer="3"),
    dict(testcase="CEIL Function",
         expression="CEIL(5.75)",
         expected_answer="6"),
    dict(testcase="ROUND Function",
         expression="ROUND(3.14)",
         expected_answer="3"),
    dict(testcase="LOWER Function",
         expression="LOWER(\"POIPOIPOI\")",
         expected_answer="poipoipoi"),
    dict(testcase="UPPER Function",
         expression="UPPER(\"poipoipoi\")",
         expected_answer="POIPOIPOI"),
    dict(testcase="CAPITALIZE Function",
         expression="CAPITALIZE(\"poipoipoi\")",
         expected_answer="Poipoipoi"),
    dict(testcase="TITLE Function",
         expression="TITLE(\"poi poi poi\")",
         expected_answer="Poi Poi Poi"),

    ]

@pytest.mark.parametrize("expression_check", expression_list)
def test_advPiping_mathExpression(create_survey, expression_check):
    driver, mySurvey, report = create_survey

    testcase = expression_check['testcase']
    expression = "{{" + expression_check['expression'] + "}}"
    expected_answer = expression_check['expected_answer']
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify advanced piping Math Expressions for ." + testcase)
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin", "Gumi"])
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, expression, 1,
                                                          ["poi", "nanodesu", "Khorosho", "desu"])
        if not mySurvey.myCreate.num_questions_in_page(2) == 1:
            mySurvey.myDesign.scroll_to_bottom()
            mySurvey.myBuilder.click_MultipleChoiceAddButton()
            mySurvey.myQuestion.enter_question_title(expression)
            mySurvey.myQuestion.enter_multipleChoice_answerText(1, "poi")
            mySurvey.myQuestion.enter_multipleChoice_answerText(2, "nanodesu")
            mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Khorosho")
            mySurvey.myQuestion.enter_multipleChoice_answerText(4, "desu")
            mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks preview button, in order to verify theme in preview window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        mySurvey.myDesign.click_off_preview_warning()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.switch_to_preview_iframe()
        mySurvey.myLogic.process_multichoice_preview(1, 1)
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title(expected_answer)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q1",
                                 "Verify question title is the same that we entered in Q1.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, u"Failed to verify question title piping for math expresssion type: " + str(testcase) + u" and string value: " + expression
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
