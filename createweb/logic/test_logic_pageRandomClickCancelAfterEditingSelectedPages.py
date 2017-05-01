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
                               "verify Randomizing all pages",  # test_suite_title
                               ("This test applies page logic "
                                " page randomization and as a random chance "
                                " to randomize selected survey pages."),  # test_suite_description
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
@pytest.mark.C212939
@pytest.mark.IB
def test_logic_pageRandomClickCancelAfterEditingSelectedPages(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify applying page random page logic for selected pages.")
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
        mySurvey.myLogic.click_PageRandomization()
        # pytest.set_trace()
        mySurvey.myLogic.pageRandom_randomizePages_selected([1, 2, 3])
        ex = mySurvey.myLogic.checkPagesRandomizedIconSelected()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page randomization icon appears",
                                 "checks to make sure that the selected page randomization icon appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page randomization icon"
        mySurvey.myLogic.click_PageRandomization()
        mySurvey.myLogic.pageRandom_randomizePages_deselectSelectedPage([2])
        mySurvey.myLogic.click_PageRandomization()
        ex = mySurvey.myLogic.pageRandom_randomizePages_verifySelected([1, 2, 3], len(pagewise_questions))
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that clicking on cancel button editing "
                                 "shouldn't save and previous state should be displayed",
                                 "checks to make sure that clicking on cancel button editing "
                                 "shouldn't save and previous state should be displayed",
                                 ex,
                                 True,
                                 not ex,
                                 driver)

        assert ex, "Failed to verify previous selected state"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
