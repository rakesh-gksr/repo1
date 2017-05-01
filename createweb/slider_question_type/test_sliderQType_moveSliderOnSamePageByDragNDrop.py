from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSliderQTypeMoveSliderOnSamePageByDragNDrop/",  # report_relative_location
                               "test_sliderQType_moveSliderOnSamePageByDragNDrop",  # report_file_name_prefix
                               "Verify move slider on the same page above or below via drag/drop",  # test_suite_title
                               ("This test adds slider question and  "
                                " move slider on the same page above or below via drag/drop"),  # test_suite_description
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
@pytest.mark.C284128
@pytest.mark.IB
def test_sliderQType_moveSliderOnSamePageByDragNDrop(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify move slider on the same page above or below "
                                                           "via drag/drop")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        slider_question_title = "Your expectation?"
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title(slider_question_title)
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that slider question is saved",
                                 "checks to make sure that slider question is saved with all required fields.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify saving of slider question"
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "How noisy is this neighborhood?")
        driver.refresh()
        mySurvey.myQuestion.dragNDropSliderToSamePage(1, 2)
        questionTitle = mySurvey.myQuestion.getQuestionTitle(2)
        if str(questionTitle) == slider_question_title:
            ex = True
        else:
            ex = False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify slider question moved to selected location "
                                                               "showing correct question title",
                                 "Verifies slider question moved to selected location showing correct question title.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify slider question moved to selected location showing correct question title"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
