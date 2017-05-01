#!/usr/bin/env python
#####################
# Author: joshuah
# Date: December 2nd, 2014
# Test Case: Verify adding multiple page skip logic
#####################
from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogic_MultiPageSkip/",  # report_relative_location
                               "test_logic_multiPage_skip",  # report_file_name_prefix
                               "Verify Multiple Page Skip Functionality",  # test_suite_title
                               ("Testing that Multi Page Skip Logic "
                                " skips proper pages as entered "
                                " and is working as intended."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_multi_page(create_survey):
    driver, mySurvey, report = create_survey

    try:
        for i in range(1, 6):
            mySurvey.myBuilder.click_NewPageAddButton()
            # time.sleep(2)
        ex = mySurvey.myLogic.get_num_pages()
        myBool = False
        if ex == 6:
            myBool = True
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Open a new survey and Add 6 new pages",
                                 "Opens a new Survey and clicks the add new page button 6 times.",
                                 myBool,
                                 True,
                                 not myBool,
                                 driver)
        assert myBool, "Failed to add 6 new pages"
        mySurvey.myLogic.unfold_LogicRegion()
        # time.sleep(1)
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        mySurvey.myLogic.select_PageSkipTypeDropdown("P3")
        mySurvey.myLogic.click_PageSkipLogicTargetApplyButton()
        myBool = False
        # time.sleep(5)
        myBool = mySurvey.myLogic.verify_page_skip_logic_applied(0, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add page skip logic to P1",
                                 "Adds page skip logic to P1 to skip to P3.",
                                 myBool,
                                 True,
                                 not myBool,
                                 driver)
        assert myBool, "Failed to add page skip logic from P1 to P3"
        mySurvey.myLogic.click_PageSkipLogicButton()
        # time.sleep(1)
        mySurvey.myLogic.select_newPageSkipLogic()
        # time.sleep(1)
        mySurvey.myLogic.select_PageSkipSelectPage("P3")
        # time.sleep(1)
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        # time.sleep(1)
        mySurvey.myLogic.select_PageSkipTypeDropdown("P5")
        # time.sleep(5)
        mySurvey.myLogic.click_PageSkipLogicTargetApplyButton()
        # time.sleep(5)
        myBool = False
        myBool = mySurvey.myLogic.verify_page_skip_logic_applied(1, 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add page skip logic to P3",
                                 "Adds page skip logic to P3 to skip to P5.",
                                 myBool,
                                 True,
                                 not myBool,
                                 driver)
        assert myBool, "Failed to add page skip logic from P3 to P5"
        mySurvey.myLogic.click_PageSkipLogicButton()
        # time.sleep(1)
        mySurvey.myLogic.select_newPageSkipLogic()
        mySurvey.myLogic.select_PageSkipSelectPage("P5")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        mySurvey.myLogic.select_PageSkipTypeDropdown("Disqualify Respondent")
        mySurvey.myLogic.click_PageSkipLogicTargetApplyButton()
        # time.sleep(5)
        myBool = False
        myBool = mySurvey.myLogic.verify_page_skip_logic_applied(2, 5)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add page skip logic to P5",
                                 "Adds page skip logic to P3 to skip to Disqualify.",
                                 myBool,
                                 True,
                                 not myBool,
                                 driver)
        assert myBool, "Failed to add page skip logic from P5 to Disqualify"
        # We are now ready to check the page skip logic on the preview page
        ex = mySurvey.myDesign.click_preview_button()

        ex = mySurvey.myDesign.switch_to_preview_window()

        ex = mySurvey.myDesign.click_off_preview_warning()
        ex = mySurvey.myDesign.click_preview_next_button()

        ex = mySurvey.myDesign.click_preview_next_button_noFrame()

        ex = mySurvey.myDesign.click_preview_next_button_noFrame()
        previewEndTitle = "That's the end of the preview!"
        myTitle = mySurvey.myDesign.getPreviewEndTitle()
        myBool = False
        if myTitle == previewEndTitle:
            myBool = True
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Open survey in Preview and test Page Skip Logic",
                                 "Opens the survey in preview mode and clicks the next button 3 times,"
                                 " this should get us to the Disqualify page.",
                                 myBool,
                                 True,
                                 not myBool,
                                 driver)
        assert myBool, "Failed to open Preview page and test logic"
        ex = mySurvey.myDesign.click_endPreview_button()
        handles = []
        handles = mySurvey.myDesign.window_check()
        myBool = False
        if len(handles) == 1:
            myBool = True
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the return to design Page",
                                 "Clicks the return to design page and closes the preview window.",
                                 myBool,
                                 True,
                                 not myBool,
                                 driver)
        assert myBool, "Failed to click return to design page"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
