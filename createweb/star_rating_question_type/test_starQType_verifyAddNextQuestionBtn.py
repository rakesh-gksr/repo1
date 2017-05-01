from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestStarQTypeVerifyAddNextQuestionBtn/",  # report_relative_location
                               "test_StarQType_verifyAddNextQuestionBtn",  # report_file_name_prefix
                               ("Verify auto saving star rating question from clicking on 'add next question' button " +
                                "on edit mode"),  # test_suite_title
                               "Test to verify adding star rating question from 'add next question' button on question "
                               "edit",
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


@pytest.mark.Star_question
@pytest.mark.BVT
@pytest.mark.IB
@pytest.mark.C812363
def test_StarQType_verifyAddNextQuestionBtn(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify adding star rating question from 'add next question'"
                                                           " button on question edit.")
    try:
        ex = mySurvey.myBuilder.click_star_rating_add_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add star rating question type to survey ",
                                 "Verified that star rating question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add star rating question to survey."
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.click_question_save_add_another()
        # code to verify that star rating question type automatically saved
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Star auto save",
                                 "Verified that star rating question type automatically saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star rating question type automatically saved."
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Another star rating question type to survey ",
                                 "Verified that another star rating question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add another star rating question to survey."
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify 2 questions Add to Live Preview",
                                 "Verifies that 2 questions added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify 2 question added to live preview."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
