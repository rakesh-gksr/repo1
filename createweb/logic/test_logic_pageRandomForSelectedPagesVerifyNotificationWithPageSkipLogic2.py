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
@pytest.mark.C212955
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
        answer_rows = ["silent", "noisy"]
        i = 0
        for question in pagewise_questions:
            mySurvey.myBank.searchForQuestion(mySurvey.survey_id, question, answer_rows)
            mySurvey.myLogic.pushQuestionToStack(question)
            mySurvey.myBuilder.unfold_BuilderRegion()
            i += 1
            if i < 5:
                mySurvey.myBuilder.click_NewPageAddButton()

        driver.refresh()
        # change question 1 type to dropdown
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.changeQType("Dropdown")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        # apply skip logic by clicking on Logic tab through hovering on question 1
        mySurvey.myQuestion.hover_on_question(1)
        mySurvey.myLogic.click_on_logic_tab_on_hovering_question()
        mySurvey.myLogic.setQuestionSkipLogic(1, 2, False, 2)

        mySurvey.myLogic.unfold_LogicRegion()
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
                                 "Verify that error notification is shown when destination page p2 is selected",
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
