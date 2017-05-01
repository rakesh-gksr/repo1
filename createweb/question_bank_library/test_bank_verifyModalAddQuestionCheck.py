from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest

input_data = [
    {
        'test_case_id': 'C280919',
        'type': 'icon_click'
     }
    ,
    {
        'test_case_id': 'C292444',
        'type': 'icon_click'
    }
]
search_keyword = "What"
open_category = "Community"


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestBankVerifyModalAddQuestion",  # report_relative_location
                               "test_bank_verifyModalAddQuestion",  # report_file_name_prefix
                               "Verify Modal Add Question Functionality",  # test_suite_title
                               "Testing of add question functionality by adding first question from modal list",  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})

    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.QBL
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C280919
@pytest.mark.C292444
@pytest.mark.parametrize("input_data", input_data, ids=[dict['test_case_id'] for dict in input_data])
def test_bank_verify_modal_add_question(create_survey, input_data):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify Add Question Functionality")
    try:
        mySurvey.myBank.unfold_QuestionBankRegion()

        ex = mySurvey.myQBank.openCategory(open_category)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify open " + open_category + " Category",
                                 "Clicks on " + open_category + " and makes sure that "
                                                                "it opens with " + open_category + " as hero button",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, open_category + " Category closing the modal failed"

        initial_question_count = mySurvey.myQBank.totalCategoryQuestions()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify default question box",
                                 "Verify default question box loaded or not",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert initial_question_count > 0, "Failed to load question box"

        if input_data['type'] == 'icon_click':
            # for icon click add question by clicking on + icon available for each question
            ex = mySurvey.myQBank.add_first_question_from_question_box_by_plus_icon_click()
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Add First Modal Question",
                                     "Verify Question added or not by click on plus icon.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to add question"
        elif input_data['type'] == 'card_click':
            # check card/box color changes or not on hover over li item
            ex = mySurvey.myQBank.check_modal_question_box_hover_color()
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Check hover effect of card",
                                     "Verify hover effect of question card.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify hover color"
            # for card click add question by clicking on card / li box  available for each question
            ex = mySurvey.myQBank.add_first_question_from_question_box_by_card_click()
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Add First Modal Question",
                                     "Verify Question added or not by click on plus icon.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to add question"
        #  check card / li box color after question add. It should be grey after question add
        ex = mySurvey.myQBank.check_modal_question_card_box_color()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check Modal Box Color",
                                 "Verify Modal Box Color of added question.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to change question card color to grey"
        # check question added into preview box or not
        ex = mySurvey.myQBank.check_modal_question_added_in_preview_box()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question in Preview Box",
                                 "Verify Added Question is added into preview box or not.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add question in preview box"
        # check question plus icon change to check icon or not after question add
        ex = mySurvey.myQBank.check_modal_question_icon_visible()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Added or Not",
                                 "Verify Question added or not based on the plus / check mark icon.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify checked icon after question add"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()