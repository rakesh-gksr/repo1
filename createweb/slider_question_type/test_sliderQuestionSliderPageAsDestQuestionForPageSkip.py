from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSliderQuestionSliderPageAsDestQuestionForPageSkip/",  # report_relative_location
                               "test_sliderQuestionSliderPageAsDestQuestionForPageSkip",  # report_file_name_prefix
                               "verify slider page can be destination question for page skip logic",  # test_suite_title
                               ("This test adds slider question and  "
                                " verify slider page can be destination question for page skip logic "),
                               # test_suite_description
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
@pytest.mark.C284121
@pytest.mark.IB
def test_sliderQuestionSliderPageAsDestQuestionForPageSkip(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify slider page can be destination question for page "
                                                           "skip logic.")
    try:
        questions = ["How noisy is this neighborhood?", "What is the question?"]
        sliderQuestiontitle = "Your expectation?"
        for question in questions:
            mySurvey.myBank.searchForQuestion(mySurvey.survey_id, question)
            mySurvey.myBuilder.click_NewPageAddButton()

        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title(sliderQuestiontitle)
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that slider question is saved on page 3",
                                 "checks to make sure that slider question is saved with all required fields.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify saving of slider question"
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(3, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question Add to Live Preview",
                                 "Verifies that Slider question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Slider question added to live preview."
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        mySurvey.myLogic.select_PageSkipTypeDropdown("P3")
        mySurvey.myLogic.click_PageSkipLogicTargetApplyButton()
        ex = mySurvey.myLogic.verify_page_skip_logic_applied(0, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Add page skip logic to P3",
                                 "Adds page skip logic to P1 to skip to P3.",
                                    ex,
                                    True,
                                    not ex,
                                    driver)
        assert ex, "Failed to add page skip logic from P2 to P1"
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Open a new survey and click the preview button",
                                 "Opens a new Survey and clicks the preview button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.click_off_preview_warning()
        mySurvey.myDesign.switch_to_preview_iframe()
        ex = mySurvey.myDesign.click_preview_next_button_noFrame()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Successfully Moved to the next page ",
                                 "Sucessfully Moved to the next page.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to move to next preview page"
        ex = mySurvey.myQuestion.verifyPreviewPageSliderQuestion(sliderQuestiontitle)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Successfully skip to the slider page ",
                                 "Verified that sucessfully skip to the slider page.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to move to slider preview page"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
