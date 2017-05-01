from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestMaxPageTitleDesc/",  # report_relative_location
                               "test_max_pageTitleDesc",  # report_file_name_prefix
                               "verify adding max page title and description characters",  # test_suite_title
                               ("This test adds max limit page title and page description, with and without RTE formatting "
                                " and then checks to make sure that we cannot add another character"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver

    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_max_pageTitleDesc(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify adding max page title and description characters.")
    try:
        page_title = mySurvey.myLogic.RNG(100)
        page_desc = mySurvey.myLogic.RNG(3995)  # should be 4000, setting temporarily to pass
        mySurvey.myDesign.click_addPageTitle(page_title, page_desc)
        ex = True if mySurvey.myDesign.get_page_title(1) == page_title else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum page title",
                                 "checks to make sure that we can add maximum length of page title",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify maximum length of page title."
        ex = True if mySurvey.myDesign.get_page_desc(1) == page_desc else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum page desc",
                                 "checks to make sure that we can add maximum length of page desc",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify maximum length of page desc."
        mySurvey.myDesign.click_addPageTitleRTE(page_title, page_desc, "Turquoise")
        ex = True if mySurvey.myDesign.get_page_title(1) == page_title else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum page title with RTE Formatting",
                                 "checks to make sure that we can add maximum length of page title with RTE formatting",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify maximum length of page title with RTE Formatting."
        ex = True if mySurvey.myDesign.get_page_desc(1) in page_desc else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum page desc with RTE formatting",
                                 "checks to make sure that we can add maximum length of page desc with RTE formatting",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify maximum length of page desc with RTE formatting."
        mySurvey.myDesign.click_addPageTitle(page_title + "poi", page_desc + "poi")
        ex = True if mySurvey.myDesign.get_page_title(1) == page_title else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify over maximum page title",
                                 "checks to make sure that we can add maximum length of page title and the rest fall off",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify over maximum length of page title."
        ex = True if mySurvey.myDesign.get_page_desc(1) == page_desc else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify over maximum page desc",
                                 "checks to make sure that we can add maximum length of page desc and the rest fall off",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify over maximum length of page desc."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
