from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.create import create_utils
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifyCollectResponsesButton",  # report_relative_location
                               "test_verifyCollectResponsesButton",  # report_file_name_prefix
                               "Verify the \"Collect Responses\" CTA in the Final state of the survey",
                               # test_suite_title
                               "Test to Verify the \"Collect Responses\" CTA in the Final state of the survey",
                               # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, "
                                                                                                      "%Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.survey_score
@pytest.mark.IB
@pytest.mark.C47650189
def test_verify_collect_responses_button(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify the \"Collect Responses\" CTA in the Final state "
                                                           "of the survey")
    try:

        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        title = mySurvey.myLogic.RNG(30)
        answerRows = []
        mySurvey.myQuestion.enter_question_title(title)
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question Add to Live Preview",
                                 "Verifies that MultipleChoice question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify MultipleChoice question added to live preview."

        ex = mySurvey.myCreate.click_survey_score()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click Rate My Survey CTA",
                                 "verifies Rate My Survey CTA present and it clicked",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that create Rate My Survey present and it clicked"
        ex = mySurvey.myCreate.verify_survey_score_modal()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Rate My Survey Modal",
                                 "verifies Rate My Survey modal box appears on screen",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Rate My Survey modal box appears on screen"

        mySurvey.myCreate.check_collect_responses_link(is_clicked=True)
        ex = "/collect/" in driver.current_url
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check Collect Responses CAT",
                                 "verifies that Collect Responses CAT appears in modal box",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Collect Responses CAT appears in modal box"

        create_utils.wait_collector_page(driver)
        ex = "/collect/" in driver.current_url
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify home page loaded",
                                 "verifies that home page loaded by clicking on Continue "
                                                               "Editing CAT",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that home page loaded by clicking on Continue Editing CAT"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
