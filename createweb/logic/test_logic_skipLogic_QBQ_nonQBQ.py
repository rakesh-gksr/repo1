from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicSkipLogicQBQNonQBQ/",  # report_relative_location
                               "test_logic_skipLogic_QBQ_nonQBQ",  # report_file_name_prefix
                               "basic: verify block updates properly inserting page within a block",  # test_suite_title
                               ("this test adds page logic and then alternates between adding QB questions and builder questions "
                                " and then verifies to make sure all questions saved succesfully."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_skipLogic_QBQ_nonQBQ(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "basic: verify block updates properly inserting page within a block.")
    try:
        mySurvey.myLogic.unfold_LogicRegion()
        # time.sleep(1)
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        mySurvey.myLogic.select_PageSkipTypeDropdown("End of Survey")
        mySurvey.myLogic.click_PageSkipLogicTargetApplyButton()
        # time.sleep(5)
        mySurvey.myBuilder.unfold_BuilderRegion()
        for x in xrange(4):
            mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myBank.unfold_QuestionBankRegion()

        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myBank.add_questionBankQuestion_via_qbsvc(
            "How noisy is this neighborhood?", mySurvey.survey_id, page_num, 1)

        mySurvey.myLogic.pushQuestionToStack("How noisy is this neighborhood?")
        mySurvey.myBuilder.unfold_BuilderRegion()
        ex = mySurvey.myBuilder.click_MultipleChoiceAddButton()
        # time.sleep(10)
        ex = mySurvey.myQuestion.enter_question_title("Best Vocaloid?")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Miku")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Luka")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Rin")
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myLogic.pushQuestionToStack("Best Vocaloid?")

        mySurvey.myBank.add_questionBankQuestion_via_qbsvc(
            "How often do you have conversations with your child about what his or her class is learning at school?", mySurvey.survey_id, page_num, 3)

        mySurvey.myLogic.pushQuestionToStack("How often do you have conversations with your child about what his or her class is learning at school?")
        mySurvey.myBuilder.unfold_BuilderRegion()
        ex = mySurvey.myBuilder.click_MatrixRatingScaleAddButton()
        ex = mySurvey.myQuestion.enter_question_title("Please classify the following Ships")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Haruna")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Yuudachi")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Naka")
        ex = mySurvey.myQuestion.enter_matrix_answerText(1, "Destroyer(DD)")
        ex = mySurvey.myQuestion.enter_matrix_answerText(2, "Light Cruiser(CL)")
        ex = mySurvey.myQuestion.enter_matrix_answerText(3, "Battleship(BB)")
        ex = mySurvey.myQuestion.enter_matrix_answerText(4, "Aircraft Carrier(CV)")
        ex = mySurvey.myQuestion.enter_matrix_answerText(5, "Submarine(SS)")
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myLogic.pushQuestionToStack("Please classify the following Ships")
        for x in xrange(4):
            ex = mySurvey.myLogic.verifyPreviewPageQuestions(x)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that question " + str(x + 1) + " saved correctly",
                                     "checks to make sure that questions saved correctly.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify question # " + str(x + 1)
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
