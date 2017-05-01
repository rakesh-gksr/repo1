from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSliderQTypeNoSupportForQuotaForSliderQuestion/",  # report_relative_location
                               "test_sliderQType_noSupportForQuotaForSliderQuestion",  # report_file_name_prefix
                               "Verify no support in quota for slider question",  # test_suite_title
                               "Test to verify no support in quota for slider question",  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.slider_question
@pytest.mark.BVT
@pytest.mark.IB
@pytest.mark.C284127
def test_sliderQType_noSupportForQuotaForSliderQuestion(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify no support in quota for slider question")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Slider question type to survey",
                                 "Verified that slider question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add slider question to survey."
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_Quota()
        ex = mySurvey.myQuestion.verify_no_support_for_quota_for_slider()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify warning message while setting quota",
                                 "Verified that warning message is displayed since can't set quota on slider question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify warning message is displayed."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

