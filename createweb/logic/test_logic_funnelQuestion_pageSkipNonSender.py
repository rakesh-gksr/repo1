from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicFunnelQuestionPageSkipNonSender/",  # report_relative_location
                               "test_logic_funnelQuestion_pageSkipNonSender",  # report_file_name_prefix
                               "Skip from non sender(located before sender) page to sender page",  # test_suite_title
                               ("This test adds a sender and receiver question and funnels accordingly."
                                " Test also adds a non sender question before the sender."
                                " Test then attempts to page skip nonsender to sender."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_funnelQuestion_newQuestionRow(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Skip from non sender(located before sender) page to sender page.")
    try:
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        ex = mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        # time.sleep(1)
        mySurvey.myBuilder.click_NewPageAddButton()
        # time.sleep(1)
        ex = mySurvey.myBuilder.click_MatrixRatingScaleAddButton()
        ex = mySurvey.myQuestion.enter_question_title("Please classify the following Ships")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Haruna")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Yuudachi")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Naka")
        mySurvey.myLogic.toggleQuestionFunneling()
        ex = mySurvey.myQuestion.enter_matrix_answerText(1, "Destroyer(DD)")
        ex = mySurvey.myQuestion.enter_matrix_answerText(2, "Light Cruiser(CL)")
        ex = mySurvey.myQuestion.enter_matrix_answerText(3, "Battleship(BB)")
        ex = mySurvey.myQuestion.enter_matrix_answerText(4, "Aircraft Carrier(CV)")
        ex = mySurvey.myQuestion.enter_matrix_answerText(5, "Submarine(SS)")
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myDesign.scroll_to_top()
        mySurvey.myBuilder.unfold_BuilderRegion()
        we = mySurvey.myQuestion.get_question_element(1)
        # time.sleep(1)
        mySurvey.myBuilder.drag_n_drop_PageBreakButton(we)
        # time.sleep(1)
        #mySurvey.myLogic.movePage(1, 2)
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        mySurvey.myLogic.select_PageSkipTypeDropdown("P3")
        mySurvey.myLogic.click_PageSkipLogicTargetApplyButton()
        ex = mySurvey.myLogic.verify_page_skip_logic_applied(0, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add page skip logic to P1",
                                 "Adds page skip logic to P1 to skip to P3.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add page skip logic from P1 to P3"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
