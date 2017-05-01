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
                               "test_logic_pageRandomWithPageSkipLogic",  # report_file_name_prefix
                               "Verify Page Randomization does not works with Page Logic when same pages are selected for rotation and Page Logic.",  # test_suite_title
                               ("This test verifies error notification is shown when same pages are selected for Page skip and randomization Logic."),  # test_suite_description
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


@pytest.mark.pagerandom
@pytest.mark.C213000
@pytest.mark.IB
def test_logic_pageRandomWithPageSkipLogic(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify Page Randomization does not works with Page Logic when same pages are selected for rotation and Page Logic.")

    try:
        pagewise_questions = [
            "How noisy is this neighborhood?",
            "In a typical month, about how much money, in U.S. dollars, do you spend on your cable service?",
            "What number would you use to rate all your health care in the last 12 months?",
            "In what state or U.S. territory are you currently registered to vote?",
            "In what county (or counties) does your target customer live?",
        ]

        # add questions and pages
        for i, question in enumerate(pagewise_questions):
            mySurvey.myBank.searchForQuestion(mySurvey.survey_id, question)
            mySurvey.myLogic.pushQuestionToStack(question)

            # dont add new page for last question
            if i != (len(pagewise_questions) - 1):
                mySurvey.myBuilder.unfold_BuilderRegion()
                mySurvey.myBuilder.click_NewPageAddButton()

        # apply page skip logic
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        mySurvey.myLogic.select_PageSkipTypeDropdown("P4")
        mySurvey.myLogic.click_PageSkipLogicTargetApplyButton()

        # verify page skip logic applied
        ex = mySurvey.myLogic.verifyPageSkipLogicStatus('On')
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Page skip logic status.",
                                 "checks to verify page skip logic status is On.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Unable to verify Page skip logic status"

        # apply page randomization for skipped page and check for error
        mySurvey.myLogic.click_PageRandomization()
        mySurvey.myLogic.pageRandom_clickOnRandomizePages()
        mySurvey.myLogic.pageRandom_randomizePages_selectPages([2, 3, 4])
        ex = mySurvey.myLogic.pageRandomVerifySkipLogicNotice()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that error notification is shown.",
                                 "checks to make sure that error notification is displayed.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify error notification"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
