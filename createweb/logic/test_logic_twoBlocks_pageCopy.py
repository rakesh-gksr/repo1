from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicTwoBlocksPageCopy/",  # report_relative_location
                               "test_logic_twoBlocks_pageCopy",  # report_file_name_prefix
                               "verify copy page from block to another block",  # test_suite_title
                               ("This test adds pages 1 and 2 to a block  and pages 3,4,5 to a different block"
                                " and then tries to copy page from block 1 to block 2"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_twoBlocks_pageCopy(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify copy page from block to another block.")
    try:
        # page1

        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "How noisy is this neighborhood?")
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()
        # page2

        mySurvey.myBank.searchForQuestion(
            mySurvey.survey_id,
            "In a typical month, about how much money, in U.S. dollars, do you spend on your cable service?")
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()
        # page3

        mySurvey.myBank.searchForQuestion(
            mySurvey.survey_id,
            "Using any number from 0 to 10, where 0 is the worst health care possible and 10"
            " is the best health care possible, what number would you use to rate all your health care in the last 12 months?")
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()
        # page4

        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "In what state or U.S. territory are you currently registered to vote?")
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()
        # page5

        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "In what county (or counties) does your target customer live?")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.click_blockRandom_newBlock()
        mySurvey.myLogic.addSequentialBlocks([1, 2])
        # time.sleep(1)
        mySurvey.myLogic.addSequentialBlocks([3, 4, 5])
        # time.sleep(5)
        mySurvey.myDesign.scroll_to_top()
        mySurvey.myLogic.copy_existing_page(1, 3)
        ex = mySurvey.myLogic.verifyBlockCreated(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify block 1 creation",
                                 "checks to make sure that block contains pages 1 and 2 and not the copied page.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify block 1 creation."
        ex = mySurvey.myLogic.verifyBlockCreated(3, 6)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify block 2 creation",
                                 "checks to make sure that block contains pages 3-6 including copied page.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify block 2 creation."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
