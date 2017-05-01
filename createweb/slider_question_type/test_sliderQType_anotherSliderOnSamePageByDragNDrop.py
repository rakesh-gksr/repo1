from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSliderQTypeAnotherSliderOnSamePageByDragNDrop/",  # report_relative_location
                               "test_sliderQType_anotherSliderOnSamePageByDragNDrop",  # report_file_name_prefix
                               "Verify move slider on the Another page above or below via drag/drop",
                               # test_suite_title
                               ("This test adds slider question and  "
                                " move slider on the Another page above or below via drag/drop"),
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
@pytest.mark.C284130
@pytest.mark.IB
def test_sliderQType_anotherSliderOnSamePageByDragNDrop(create_survey):
    driver, mySurvey, report = create_survey
    driver.set_window_size(1920,1080)

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify move slider on the Another page above or below "
                                                           "via drag/drop")
    try:
        slider_question_title = "This is slider question"
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "This is slider question")
        mySurvey.myBuilder.unfold_BuilderRegion()
        ex = mySurvey.myBuilder.click_NewPageAddButton()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify New Page add",
                                 "Verifies that new page added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify new page added to survey."
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "How noisy is this neighborhood?")
        driver.refresh()
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.changeQType("Slider")
        ex = mySurvey.myQuestion.verify_question_in_edit_mode('question-open-ended-single', 'slider')
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Type Switched to Slider Question",
                                 "Verifies that question type switched to Slider",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question type switched to Slider."
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question is added to Slider question",
                                 "checks that question is added to Slider question.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question is updated to slider question."
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question Add to Live Preview",
                                 "Verifies that Slider question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Slider question added to live preview."
        driver.execute_script("document.body.style.transform = 'scale(0.5)';")
        mySurvey.myQuestion.dragNDropSliderToAnotherPage(1)
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(2, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify after moving Slider question "
                                                               "count of second page becomes two",
                                 "Verifies that after moving Slider question count of the second page becomes two",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Slider question added to second page."
        questionTitle = mySurvey.myQuestion.getQuestionTitle(1)
        if str(questionTitle) == slider_question_title:
            ex = True
        else:
            ex = False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question number after drag drop",
                                 "Verifies that Slider after drag drop.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Slider after drag drop."

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
