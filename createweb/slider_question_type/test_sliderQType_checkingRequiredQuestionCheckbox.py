from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSliderQTypeCheckingRequiredQuestionCheckbox/",  # report_relative_location
                               "test_sliderQType_checkingRequiredQuestionCheckbox",  # report_file_name_prefix
                               "Verify making slider question required - option tab",  # test_suite_title
                               ("This test adds slider question and  "
                                " Verify making slider question required - option tab"),  # test_suite_description
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
@pytest.mark.C284116
@pytest.mark.IB
def test_sliderQType_checkingRequiredQuestionCheckbox(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify making slider question required - option tab.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title("Your expectation?")
        mySurvey.myQuestion.click_question_options_tab()
        mySurvey.myQuestion.toggle_answer_required()
        ex = mySurvey.myQuestion.verify_required_option()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider Question Required Option is Turned on",
                                 "Verifies that slider question required option is turned on",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify slider question required option is turned on"
        ex = mySurvey.myQuestion.click_question_save_from_options_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that slider question is saved by making"
                                                               " slider question as required",
                                 "checks to make sure that slider question is saved by making slider question "
                                 "as required.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify saving of slider question"
        ex = mySurvey.myQuestion.verify_question_required(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that slider question has required symbol (*)",
                                 "checks to make sure that slider question has required symbol (*).",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify required symbol(*) on question"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
