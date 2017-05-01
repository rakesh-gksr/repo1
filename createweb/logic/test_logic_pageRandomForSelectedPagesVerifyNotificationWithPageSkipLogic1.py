from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest

__author__ = 'mangesh'

@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicPageRandomSelected/",  # report_relative_location
                               "test_logic_pageRandomSelected",  # report_file_name_prefix
                               "verify notification when page has skip logic",  # test_suite_title
                               ("This test verifies notification when page has/hasn't skip logic"),  # test_suite_description
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

@pytest.mark.pageRandomization
@pytest.mark.C212953
@pytest.mark.IB
def test_logic_pageRandomSelectedPagesVerifynotificationWithPageSkipLogic(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify notificaiton on page randomization while"
                                                           " randomizing selected page which is/isn't destination page")
    try:
        pagewise_questions = [
            "How noisy is this neighborhood?",
            "In a typical month, about how much money, in U.S. dollars, do you spend on your cable service?",
            "What number would you use to rate all your health care in the last 12 months?",
            "In what state or U.S. territory are you currently registered to vote?",
            "In what county (or counties) does your target customer live?",
        ]
        i = 0
        for question in pagewise_questions:
            mySurvey.myBank.searchForQuestion(mySurvey.survey_id, question)
            mySurvey.myLogic.pushQuestionToStack(question)
            mySurvey.myBuilder.unfold_BuilderRegion()
            i += 1
            if i < 5:
                mySurvey.myBuilder.click_NewPageAddButton()

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        mySurvey.myLogic.select_PageSkipTypeDropdown("P2")
        mySurvey.myLogic.click_PageSkipLogicTargetApplyButton()
        # check for page skip logic status
        ex = mySurvey.myLogic.verifyPageSkipLogicStatus('On')
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Page skip logic status.",
                                 "checks to verify page skip logic status is On.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Unable to verify Page skip logic status"

        mySurvey.myLogic.click_PageRandomization()
        mySurvey.myLogic.pageRandom_clickOnRandomizePages()
        mySurvey.myLogic.pageRandom_randomizePages_selectPages([1, 3])
        ex = mySurvey.myLogic.pageRandomVerifySkipLogicNotice(False)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that error notification is not shown"
                                                               " when p1 and p3 page selected",
                                 "checks to make sure that error notification is not displayed.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify error notification"
        mySurvey.myLogic.pageRandom_randomizePages_selectPages([2])
        ex = mySurvey.myLogic.pageRandomVerifySkipLogicNotice()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that error notification is shown when destination p2 page selected",
                                 "checks to make sure that error notification is displayed.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify error notification"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
