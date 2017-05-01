from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from smsdk.qafw.rpage import pyramidsurveypage as Spage
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSliderQuestionSliderQuestionAsDestQuestionForQuestionSkip/",
                               # report_relative_location
                               "test_sliderQuestionSliderQuestionAsDestQuestionForQuestionSkip",
                               # report_file_name_prefix
                               "verify slider can be destination question for question skip logic",  # test_suite_title
                               ("This test adds slider question and  "
                                " verify slider can be destination question for question skip logic "),
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
def test_sliderQuestionSliderQuestionAsDestQuestionForQuestionSkip(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify slider can be destination question for question "
                                                           "skip logic.")
    try:
        sliderQuestiontitle = "Your expectations?"
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_dropdown_question(
            mySurvey.survey_id, page_num,
            "Best KanMusu", 1, ["Yuudachi", "Naka", "Prinz Eugen"])

        ex = mySurvey.myBuilder.click_NewPageAddButton()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add New Page",
                                 "checks to make sure that page 2 added to survey.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify page 2 added to survey"

        mySurvey.myBuilder.click_NewPageAddButton()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add New Page",
                                 "checks to make sure that page 3 added to survey.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify page 3 added to survey"
        page_num = mySurvey.myDesign.getPageID(3)
        mySurvey.myQuestion.generate_menu_matrix_question(
            mySurvey.survey_id, page_num,
            "How is it?", 1)
        mySurvey.myLogic.move_to_new_page(3)
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
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(3, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question Add to Live Preview",
                                 "Verifies that Slider question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Slider question added to live preview."
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.click_question_logic_tab()
        mySurvey.myLogic.setQuestionSkipLogic(1, 3, False, 3)

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
        # select 1st dropdown answer
        mySurvey.myDesign.switch_to_preview_iframe()
        Spage.take_survey(driver, { 1: {'choices_list': ['Yuudachi']}})
        ex = mySurvey.myDesign.click_preview_next_button_noFrame()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Successfully Moved to the next page ",
                                 "Sucessfully Moved to the next page.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to move to next preview page"
        ex = mySurvey.myQuestion.verifyPreviewPageSliderQuestion(sliderQuestiontitle)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Successfully skip to the slider question ",
                                 "Verified that sucessfully skip to the slider question.",
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
