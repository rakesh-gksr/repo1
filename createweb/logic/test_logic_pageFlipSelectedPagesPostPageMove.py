from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicPageFlipSelected/",  # report_relative_location
                               "test_logic_pageFlipSelectedPagesPostPageMove",  # report_file_name_prefix
                               "verify flip pages with selected pages after moving pages",  # test_suite_title
                               ("This test applies page logic "
                                " page flip and checks pages available "
                                " post page move"),  # test_suite_description
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

@pytest.mark.IB
@pytest.mark.pageflip
@pytest.mark.TC_15
def test_logic_pageFlipSelectedPagesPostPageMove(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify applying page flip page logic.")
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

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageRandomization()

        mySurvey.myLogic.pageRandom_flipPages_selected([1, 3, 5], len(pagewise_questions))

        # check page randomization icons
        ex = mySurvey.myLogic.checkPagesRandomizedIconSelected()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page randomization icon appears",
                                 "checks to make sure that the page randomization icon appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page randomization icon"

        # move page
        mySurvey.myLogic.movePage(1, 5, "after")

        # check selected page randomization post page move
        mySurvey.myLogic.click_PageRandomization()
        ex = mySurvey.myLogic.pageRandom_flipPages_verifySelected([2, 4, 5], len(pagewise_questions))
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that page flip for selected pages post move works",
                                 "checks to make sure that post page move, selected page flip list is proper.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify correct page list shown for page flip option post page move."

        # check page randomization icons post page move
        ex = mySurvey.myLogic.checkPagesRandomizedIconSelected()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page randomization icon appears",
                                 "checks to make sure that the page randomization icon appears post page move.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page randomization icon post page move"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
