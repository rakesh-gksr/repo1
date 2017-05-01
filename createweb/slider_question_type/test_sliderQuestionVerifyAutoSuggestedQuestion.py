from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSliderQuestionVerifyAutoSuggestedQuestion.py/",  # report_relative_location
                               "test_sliderQuestionVerifyAutoSuggestedQuestion",  # report_file_name_prefix
                               "verify auto suggested questions on slider edit mode",  # test_suite_title
                               ("This test adds slider question and  "
                                " verify auto suggested questions on slider edit mode "),  # test_suite_description
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
@pytest.mark.C284141
@pytest.mark.IB
def test_sliderQuestionVerifyAutoSuggestedQuestion(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify auto suggested questions on slider edit mode.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title("what", True)
        ex = mySurvey.myQuestion.verifyAutoSuggestedTitle()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that auto suggested question is showing"
                                                               " for slider question",
                                 "checks to make sure that auto suggested question shown on slider edit mode.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify auto suggested questions on slider edit mode"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
