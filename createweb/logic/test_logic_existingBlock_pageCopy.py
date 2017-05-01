from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicExistingBlockPageCopy/",  # report_relative_location
                               "test_logic_existingBlock_pageCopy",  # report_file_name_prefix
                               "verify copy page within a block",  # test_suite_title
                               ("This test adds pages 1 and 2 to a block "
                                " and then tries to copy page 1 before page 2 and verify it is added to the block"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_existingBlock_pageCopy(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify copying page within a block.")
    try:
        # page1

        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "How noisy is this neighborhood?")
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()
        # page2

        mySurvey.myBank.searchForQuestion(
            mySurvey.survey_id,
            "In a typical month, about how much money, in U.S. dollars, do you spend on your cable service?")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.click_blockRandom_newBlock()
        mySurvey.myLogic.addSequentialBlocks([1, 2])
        # time.sleep(1)
        mySurvey.myCreate.scroll_to_page_num(1)
        mySurvey.myLogic.copy_existing_page(1, 2, "Before")
        ex = mySurvey.myLogic.verifyBlockCreated(1, 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that new page added to block",
                                 "checks to make sure that page copied page is added to the block.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify new copied page added to block."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
