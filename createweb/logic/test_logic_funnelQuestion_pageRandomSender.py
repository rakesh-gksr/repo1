from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicFunnelQuestionPageRandomSender/",  # report_relative_location
                               "test_logic_funnelQuestion_pageRandomSender",  # report_file_name_prefix
                               "Randomize Page with sender question with all other pages that are also after the page with the receiver question.",  # test_suite_title
                               ("This test adds a sender and receiver question with one funneled into the other "
                                " Test then verifies that page randomization cannot be applied on sender page."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_funnelQuestion_pageRandomSenderAfter(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Randomize Page with sender question with all other pages that are also after the page with the receiver question..")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myBuilder.click_MatrixRatingScaleAddButton()
        mySurvey.myQuestion.enter_question_title("Please classify the following Ships")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Haruna")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Yuudachi")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Naka")
        mySurvey.myLogic.toggleQuestionFunneling()
        mySurvey.myQuestion.enter_matrix_answerText(1, "Destroyer(DD)")
        mySurvey.myQuestion.enter_matrix_answerText(2, "Light Cruiser(CL)")
        mySurvey.myQuestion.enter_matrix_answerText(3, "Battleship(BB)")
        mySurvey.myQuestion.enter_matrix_answerText(4, "Aircraft Carrier(CV)")
        mySurvey.myQuestion.enter_matrix_answerText(5, "Submarine(SS)")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myLogic.verifyNumFunneledRows(3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Funneled Rows",
                                 "checks to make sure that there are now 3 total funneled questions in the survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify total funneled rows."
        for x in xrange(3):
            mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageRandomization()
        mySurvey.myLogic.pageRandom_randomizePages_selected([1])
        ex = mySurvey.myLogic.verify_pageRandom_randomizePages_conflictError()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify page randomization conflict error",
                                 "checks to make sure that the conflict error appears in page randomization",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify conflict error on page randomization page."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

def test_logic_funnelQuestion_pageRandomSenderBefore(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Randomize Page with sender question with all other pages that are also after the page with the receiver question..")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myBuilder.click_MatrixRatingScaleAddButton()
        mySurvey.myQuestion.enter_question_title("Please classify the following Ships")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Haruna")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Yuudachi")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Naka")
        mySurvey.myLogic.toggleQuestionFunneling()
        mySurvey.myQuestion.enter_matrix_answerText(1, "Destroyer(DD)")
        mySurvey.myQuestion.enter_matrix_answerText(2, "Light Cruiser(CL)")
        mySurvey.myQuestion.enter_matrix_answerText(3, "Battleship(BB)")
        mySurvey.myQuestion.enter_matrix_answerText(4, "Aircraft Carrier(CV)")
        mySurvey.myQuestion.enter_matrix_answerText(5, "Submarine(SS)")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myLogic.verifyNumFunneledRows(3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Funneled Rows",
                                 "checks to make sure that there are now 3 total funneled questions in the survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify total funneled rows."
        mySurvey.myDesign.scroll_to_top()
        for x in xrange(3):
            mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageRandomization()
        mySurvey.myLogic.pageRandom_randomizePages_selected([1])
        ex = mySurvey.myLogic.verify_pageRandom_randomizePages_conflictError()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify page randomization conflict error",
                                 "checks to make sure that the conflict error appears in page randomization",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify conflict error on page randomization page."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
