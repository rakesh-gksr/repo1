from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):

    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSQTSingleTextboxNewQuestion/",  # report_relative_location
                               "test_SQT_singleTextbox_newQuestion",  # report_file_name_prefix
                               "verify autosaving switched question type while adding another from builder ",  # test_suite_title
                               ("This test suite adds a a multiple choice question and switches it to a single textbox   "
                                " Test verifies question saved when new question added during editing."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_SQT_singleTextbox_newQuestion(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify autosaving switched question type while adding another from builder")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.changeQType("SingleTextbox")
        answerRows = []
        matrixRows = []
        title = mySurvey.myLogic.RNG(30)
        mySurvey.myQuestion.enter_question_title(title)
        mySurvey.myBuilder.click_MatrixRatingScaleAddButton()
        mySurvey.myDesign.scroll_to_bottom()
        mySurvey.myQuestion.click_question_cancel_from_edit_tab()
        mySurvey.myDesign.scroll_to_top()
        ex = True if mySurvey.myQuestion.verifyQuestionTitle(1) == title else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify title is correct",
                                 "verifies that the title of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify title"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
