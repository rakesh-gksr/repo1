from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSliderQTypeVerifyDefaultScaleRange/",  # report_relative_location
                               "test_sliderQType_verifyDefaultScaleRange",  # report_file_name_prefix
                               "Verify survey creator should be able to define scale range between 0-100 - option tab",
                               # test_suite_title
                               "Test to Verify survey creator should be able to define scale range between "
                               "0-100 - option tab",
                               # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d,"
                                                                                                      " %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.slider_question
@pytest.mark.BVT
@pytest.mark.IB
@pytest.mark.C284113
def test_sliderQType_verifyDefaultScaleRange(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify survey creator should be able to define scale "
                                                           "range between 0-100 - option tab.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.click_question_options_tab()
        mySurvey.myQuestion.checkSliderScaleCheckbox()
        min = mySurvey.myQuestion.get_text_of_scal_value('SliderMinRangeTextbox')
        max = mySurvey.myQuestion.get_text_of_scal_value('SliderMaxRangeTextbox')
        ex = True if (min == str(0) and max == str(100)) else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Default Scale Range Shows 0 -100",
                                 "Verified that slider question default scale range shows 0 -100",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify slider question default scale range shows 0 -100."

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

