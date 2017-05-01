from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSQTMoveNewPage/",  # report_relative_location
                               "test_SQT_moveNewPage",  # report_file_name_prefix
                               "Move switched question to different page",  # test_suite_title
                               ("This test adds a dropdown question and switches it to a matrix question.  "
                                " Test moves question to a new page and verifies this."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_SQT_moveNewPage(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Move switched question to different page")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_DropdownAddButton()
        title = mySurvey.myLogic.RNG(30)
        mySurvey.myQuestion.enter_question_title(title)
        mySurvey.myQuestion.changeQType("Matrix")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_matrix_answerText(1, mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.click_question_move_tab()
        mySurvey.myLogic.moveQuestion(2, 1)
        ex = True if mySurvey.myCreate.num_questions_in_page(1) == 0 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify page 1 empty",
                                 "verifies that the question was moved from page 1",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question move from page 1"
        ex = True if mySurvey.myCreate.num_questions_in_page(2) == 1 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verifies question added to page 2",
                                 "Verifies that the question was moved to page 2",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question moved"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
