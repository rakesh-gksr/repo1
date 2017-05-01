from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifyClosingModalBox/",  # report_relative_location
                               "test_verifyClosingModalBox",  # report_file_name_prefix
                               "Verify Rate my survey CTA, and opening/closing the rate my survey modal box.",
                               # test_suite_title
                               "Test to verify Rate my survey CTA, and opening/closing the rate my survey modal box.",
                               # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, "
                                                                                                      "%Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.survey_score
@pytest.mark.IB
@pytest.mark.C46820426
@pytest.mark.C46820428
@pytest.mark.C46820429
@pytest.mark.C46820430
def test_step1_verify_closing_modal_box(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(
        ReportMessageTypes.TEST_CASE, "Verify closing the modal by \"x\" button on the top right corner of the modal.")
    try:
        ex = mySurvey.myCreate.click_survey_score()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check Rate My Survey CTA",
                                 "verifies Rate My Survey CTA present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that create Rate My Survey present"
        ex = mySurvey.myCreate.verify_survey_score_modal()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Rate My Survey Modal",
                                 "verifies Rate My Survey modal box appears on screen",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Rate My Survey modal box appears on screen"

        ex = mySurvey.myCreate.close_survey_score_modal("CloseSurveyScoreModal")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Closing modal box by x button ",
                                 "verifies that modal box is closed by clicking on x button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that modal box is closed by clicking on x button"
        mySurvey.myCreate.click_survey_score()
        ex = mySurvey.myCreate.verify_survey_score_modal()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Reopen Rate My Survey Modal",
                                 "verifies Rate My Survey Modal appears on screen.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Rate My Survey Modal appears on screen"

        ex = mySurvey.myCreate.close_survey_score_modal("CloseSurveyScoreByClickOutside")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Closing modal box by clicking outside the modal box",
                                 "verifies that modal box is closed by clicking outside the modal box.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that modal box is closed by clicking outside the modal box"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
