from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestadvBranchVerifyTooltip/",  # report_relative_location
                               "test_advBranch_verifyToolTip",  # report_file_name_prefix
                               "Verify hovering on tooltip",
                               # test_suite_title
                               "This test verifies that tooltip display when hovering on tooltip icon.",
                               # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init("platinum_advanced_branching")
    import datetime
    import os
    testcasename = os.path.basename(__file__).split(".")[0] + "--" + datetime.datetime.now().strftime("%I:%M%p %b %d,"
                                                                                                      " %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.advBranch
@pytest.mark.IB
@pytest.mark.C225167
def test_advBranch_verifyToolTip(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify hovering on tooltip")
    try:
        # below code click on page logic drop down
        mySurvey.myCreate.select_page_logic_from_dropdown()
        # below code verifies that tooltip icon is visible or not
        ex = mySurvey.myCreate.verify_adv_branch_tooltip_visible()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verifies advance branching tooltip ? icon is visible",
                                 "Verifies that the tooltip icon for advance branching is visible",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify tooltip icon for advance branching is displayed"
        # below code hover over the advance branch tooltip icon
        mySurvey.myCreate.hover_on_adv_branch_tooltip()
        # below code verifies that tooltip message is displayed or not
        ex = mySurvey.myCreate.verify_adv_branch_tooltip_message()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify tooltip message for advance branching",
                                 "Verifies that advance branching tooltip message appears",
                                 ex,
                                 True,
                                 not ex,
                                 driver)

        assert ex, "Failed to verify advance branching tooltip message"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


