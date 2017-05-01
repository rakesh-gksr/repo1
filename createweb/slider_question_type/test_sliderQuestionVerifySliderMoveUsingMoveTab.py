from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSliderQuestionVerifySliderMoveUsingMoveTab/",  # report_relative_location
                               "test_sliderQuestionVerifySliderMoveUsingMoveTab",  # report_file_name_prefix
                               "move slider on the same page above or below using move tab "
                               "condition dropdown - no support for slider",  # test_suite_title
                               ("This test adds slider question and  "
                                " move slider on the same page above or below using move tab"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os

    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime(
        "%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()

    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.slider_question
@pytest.mark.C284129
@pytest.mark.IB
def test_sliderQuestionVerifySliderMoveUsingMoveTab(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "move slider on the same page above or below using move tab")
    try:
        question_title = "Your expectation?"
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title(question_title)
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that slider question is saved",
                                 "checks to make sure that slider question is saved with all required fields.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify saving of slider question"
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question Add to Live Preview",
                                 "Verifies that Slider question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Slider question added to live preview."
        mySurvey.myBuilder.click_SingleTextboxAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Single Textbox question Add to Live Preview",
                                 "Verifies that Single Textbox question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Single Textbox question added to live preview."
        mySurvey.myQuestion.hover_on_question(1)
        mySurvey.myQuestion.click_on_move_tab_on_hovering_question()
        mySurvey.myLogic.moveQuestion(1, 1)
        driver.refresh()
        ex = mySurvey.myQuestion.verifyQuestionNumber(2, "2. "+question_title)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that slider is moved to selected location showing correct question number",
                                 "checks to make sure that slider is moved to selected location showing correct "
                                 "question number",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify slider is moved to selected location showing correct question number"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
