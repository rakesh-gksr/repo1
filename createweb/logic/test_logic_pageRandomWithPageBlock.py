from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicPageRandomSelected/",  # report_relative_location
                               "test_logic_pageRandomWithPageBlock",  # report_file_name_prefix
                               "verify pages shows on selected page randomization dropdown after removing them from blocks",  # test_suite_title
                               "This test adds blocks and checks if pages availabe for page randomization is correct or not", # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.IB
@pytest.mark.pagerandom
@pytest.mark.C212948
def test_logic_newBlock_addLogic(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "To verify pages shows on selected page randomization dropdown after removing them from blocks.")
    try:
        # add few pages
        pagewise_questions = [
            "How noisy is this neighborhood?",
            "In a typical month, about how much money, in U.S. dollars, do you spend on your cable service?",
            "What number would you use to rate all your health care in the last 12 months?",
            "In what state or U.S. territory are you currently registered to vote?",
            "Do you feel your children is getting proper education facilities?",
            "What is average payout for a fresher in your field?",
        ]
        # add questions and pages
        for i, question in enumerate(pagewise_questions):
            mySurvey.myBank.searchForQuestion(mySurvey.survey_id, question)
            mySurvey.myLogic.pushQuestionToStack(question)

            # dont add new page for last question
            if i != (len(pagewise_questions) - 1):
                mySurvey.myBuilder.unfold_BuilderRegion()
                mySurvey.myBuilder.click_NewPageAddButton()

        # add block for Page 1 and 2
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.click_blockRandom_newBlock()
        mySurvey.myLogic.addSequentialBlocks([1, 2])
        # verify block creation
        ex = mySurvey.myLogic.verifyBlockCreated(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify block 1 creation",
                                 "checks to make sure that block 1 creation occured with pages 1 and 2.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify block 1 creation."

        # create block for Page 2 and Page 3 and verify
        mySurvey.myLogic.addSequentialBlocks([3, 4])
        ex = mySurvey.myLogic.verifyBlockCreated(3, 4)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify block 2 creation",
                                 "checks to make sure that block 2 creation with pages 3 and 4.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify block 2 creation."

        mySurvey.myLogic.blockRandomDone()

        # check pages added in block are not available for page randomization
        mySurvey.myLogic.click_PageRandomization()
        ex = mySurvey.myLogic.pageRandom_randomizePages_verifyPagesNotAvailable([1, 2, 3, 4])
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that pages added in block is not available",
                                 "checks if pages added in block is not available for page randomization",
                                 ex,
                                 True,
                                 not ex,
                                 driver)

        assert ex, "Failed to verify pages added in block is not available"

        # check pages which is not part of block are available for page randomization
        ex = mySurvey.myLogic.pageRandom_randomizePages_verifyPagesAvailable([5, 6])
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that pages not added in block is available",
                                 "checks if pages which are not added in block is available for page randomization",
                                 ex,
                                 True,
                                 not ex,
                                 driver)

        assert ex, "Failed to verify pages available for page randomization"

        # remove the page blocks
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.click_blockRandomization_editBlock()
        ex = mySurvey.myLogic.click_blockRandomization_killBlock([1, 2])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify first block deletion",
                                 "checks to make sure that block deleted.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify first block deletion."

        ex = mySurvey.myLogic.click_blockRandomization_killBlock([3, 4])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify second block deletion",
                                 "checks to make sure that block deleted.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify second block deletion."

        mySurvey.myLogic.blockRandomDone()
        mySurvey.myLogic.click_PageRandomization()

        # check all pages are available for page randomization
        ex = mySurvey.myLogic.pageRandom_randomizePages_verifyPagesAvailable([1, 2, 3, 4, 5, 6])
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that all pages are available for page randomization",
                                 "checks if all pages are available for page randomization",
                                 ex,
                                 True,
                                 not ex,
                                 driver)

        assert ex, "Failed to verify that all pages are available for page randomization"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
