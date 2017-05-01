from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifyAddFirstQuestion",  # report_relative_location
                               "test_verifyAddFirstQuestion",  # report_file_name_prefix
                               "Verify the 'Add First Question' CTA present or not in the survey recommendation panel",
                               # test_suite_title
                               ("Test to verify the 'Add First Question' CTA present or not in the survey "
                                "recommendation panel"),
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
@pytest.mark.C47650185
@pytest.mark.C48262944
def test_verify_add_first_question(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify the \"Add First Question\" CTA present in "
                                                           "the survey recommendation panel")
    try:
        ex = mySurvey.myCreate.click_survey_score()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check Rate My Survey CTA",
                                 "verifies Rate My Survey CTA present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that create Rate My Survey present"
        ex = mySurvey.myCreate.verify_survey_score_modal()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Rate My Survey Modal",
                                 "verifies Rate My Survey modal box appears on screen",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Rate My Survey modal box appears on screen"
        ex = not mySurvey.myCreate.verify_survey_recommendation()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify No Survey Recommendation",
                                 "verifies Survey Recommendation is not present if survey is blank",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Survey Recommendation is not present if survey is blank"

        ex = mySurvey.myCreate.verify_add_question_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Add First Question CTA",
                                 "verifies Add First Question CTA present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Add First Question CTA present"

        ex = mySurvey.myCreate.click_add_question_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Add First Question CTA",
                                 "verifies Add First Question CTA present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Add First Question CTA present"

        ex = mySurvey.myQuestion.verify_question_in_edit_mode()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Multiple Choice question",
                                 "checks multiple choice question is added",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify multiple choice question is added."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.survey_score
@pytest.mark.IB
@pytest.mark.C47650186
def test_verify_add_first_question_not_present(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE,
                             "Verify the \"Add First Question\" CTA is not present in the survey recommendation "
                             "panel when atleast one question is present in the survey")
    try:
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
        ex = not mySurvey.myCreate.verify_survey_recommendation()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify No Survey Recommendation",
                                 "verifies Survey Recommendation is not present if survey is blank",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Survey Recommendation is not present if survey is blank"

        ex = mySurvey.myCreate.verify_add_question_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Add First Question CTA",
                                 "verifies Add First Question CTA present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Add First Question CTA present"

        ex = mySurvey.myCreate.click_add_question_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Add First Question CTA",
                                 "verifies Add First Question CTA present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Add First Question CTA present"

        ex = mySurvey.myQuestion.verify_question_in_edit_mode()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Multiple Choice question",
                                 "checks multiple choice question is added",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify multiple choice question is added."

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

        ex = not mySurvey.myCreate.verify_add_question_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Add First Question CTA not shown",
                                 "verifies that Add First Question CTA not shown if survey have at least 1 question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Add First Question CTA not shown if survey have at least 1 question"

        ex = mySurvey.myCreate.close_survey_score_modal("CloseSurveyScoreModal")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Closing modal box by x button ",
                                 "verifies that modal box is closed by clicking on x button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that modal box is closed by clicking on x button"

        mySurvey.myQuestion.hover_on_question_to_delete_it()
        ex = True if mySurvey.myCreate.num_questions_in_page(1) == 0 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question deletion",
                                 "verifies that the question was deleted from the survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question deletion"

        ex = mySurvey.myCreate.click_survey_score()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click Rate My Survey CTA",
                                 "verifies Rate My Survey CTA present and it clicked",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that create Rate My Survey present and it clicked"
        ex = mySurvey.myCreate.verify_add_question_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Add First Question CTA",
                                 "verifies Add First Question CTA present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Add First Question CTA present"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
