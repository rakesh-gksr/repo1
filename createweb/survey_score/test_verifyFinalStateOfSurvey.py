from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifyFinalStateOfSurvey",  # report_relative_location
                               "test_verifyFinalStateOfSurvey",  # report_file_name_prefix
                               "Verify the Final state of the survey, survey recommendation panel "
                               "has \"Collect Responses\" CTA",
                               # test_suite_title
                               ("Test to verify the Final state of the survey, survey recommendation panel "
                                "has \"Collect Responses\" CTA"),
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
@pytest.mark.C47650188
def test_verify_final_state_of_survey(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify the Final state of the survey, survey "
                                                           "recommendation panel has \"Collect Responses\" CTA")
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

        ex = mySurvey.myCreate.check_recommendation_message()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check Recommendation Message",
                                 "verifies Recommended message appears in modal box",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Recommended message appears in modal box"

        ex = mySurvey.myCreate.check_collect_responses_link()

        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check Collect Responses CAT",
                                 "verifies that Collect Responses CAT appears in modal box",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Collect Responses CAT appears in modal box"

        ex = mySurvey.myCreate.check_continue_editing_link()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check Continue Editing CAT",
                                 "verifies that Continue Editing CAT appears in modal box",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Continue Editing CAT appears in modal box"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
