from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from smsdk.qafw.create.create_start import click_step_1_radio_button
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestStarQTypeCoypSurvey/",  # report_relative_location
                               "test_starQType_copySurvey",  # report_file_name_prefix
                               "Make sure copying existing survey with star copies star as expected",
                               # test_suite_title
                               "This test verifies copying existing survey with star question",
                               # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init('platinum_default')
    import datetime
    import os
    testcasename = datetime.datetime.now().strftime("%I:%M%p %b %d, %Y") + '--' + os.path.basename(__file__).split('.')[
        0]

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.star_question
@pytest.mark.BVT
@pytest.mark.IB
@pytest.mark.C812391
def test_starQType_copySurvey(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Make sure copying existing survey with star copies "
                                                           "star as expected")
    try:
        survey_title = mySurvey.myCreate.get_survey_title()
        question_title = mySurvey.myLogic.RNG(30)
        mySurvey.myBuilder.click_star_rating_add_button()
        mySurvey.myQuestion.enter_question_title(question_title)
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()

        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Star question type to survey",
                                 "Verified that star question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add star question to survey."
        # Code to create new survey
        mySurvey.myDesign.scroll_to_top()
        mySurvey.myCreate.click_new_survey()
        click_step_1_radio_button(driver, 2)
        ex = mySurvey.myCreate.choose_first_existing_survey(survey_title)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verifying Copying Existing Survey",
                                 "Verified that copying existing survey with star question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify copying existing survey with star question."
        mySurvey.myQuestion.click_on_question_to_edit()
        ex = mySurvey.myQuestion.verify_question_in_edit_mode("question-emoji-rating")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Star Question Exist In Survey",
                                 "Verifies that star question exist in survey.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star question exist in survey."
        ex = mySurvey.myQuestion.verifyQuestionTitleString(question_title)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title",
                                 "Verifies that star question title matched.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star question title matched."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
