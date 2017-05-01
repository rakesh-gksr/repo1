from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSQTDeleteRestore/",  # report_relative_location
                               "test_SQT_deleteRestore",  # report_file_name_prefix
                               "delete and restore switched question",  # test_suite_title
                               ("This test adds a single textbox question and switches it to a multi choice.  "
                                " Test deletes and adds question back and verifies this was done."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_SQT_deleteRestore(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "delete and restore switched question")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SingleTextboxAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.changeQType("MultipleChoice")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = True if mySurvey.myCreate.num_questions_in_page(1) == 1 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify 1 question present on the page",
                                 "Verifies we added the question to the survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question added"
        mySurvey.myQuestion.hover_on_question_to_delete_it()
        ex = True if mySurvey.myCreate.num_questions_in_page(1) == 0 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question deletion",
                                 "verifies that the question was deleted from the survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question deletion"
        mySurvey.myCreate.restoreDeletedQuestion(1)
        ex = True if mySurvey.myCreate.num_questions_in_page(1) == 1 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verifies question added back",
                                 "Verifies that we added the question back to the survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question re-added"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
