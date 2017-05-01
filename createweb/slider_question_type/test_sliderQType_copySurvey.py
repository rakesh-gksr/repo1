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
                               "TestSliderQTypeCoypSurvey/",  # report_relative_location
                               "test_sliderQType_copySurvey",  # report_file_name_prefix
                               "Make sure copying existing survey with slider copies slider as expected",
                               # test_suite_title
                               "This test verifies copying existing survey with slider question",
                               # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init('platinum_default')
    import datetime
    import os
    testcasename = datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")+ '--' + os.path.basename(__file__).split('.')[0]

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.slider_question
@pytest.mark.BVT
@pytest.mark.IB
@pytest.mark.C284136
def test_sliderQType_copySurvey(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Make sure copying existing survey with slider copies "
                                                           "slider as expected")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        survey_title = mySurvey.myCreate.get_survey_title()
        question_title = mySurvey.myLogic.RNG(30)
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title(question_title)
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)

        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Slider question type to survey",
                                 "Verified that slider question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add slider question to survey."
        # Code to create new survey
        mySurvey.myDesign.scroll_to_top()
        mySurvey.myCreate.click_new_survey()
        click_step_1_radio_button(driver, 2)
        ex = mySurvey.myCreate.choose_first_existing_survey(survey_title)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verifying Copying Existing Survey",
                                 "Verified that copying existing survey with slider question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify copying existing survey with slider question."
        mySurvey.myQuestion.click_on_question_to_edit()
        ex = mySurvey.myQuestion.verifySliderQuestionType(question_title)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider Question Exist In Survey",
                                 "Verifies that slider question exist in survey.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify slider question exist in survey."


    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

