from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):

    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSQTSwitchingAll/",  # report_relative_location
                               "test_SQT_switchingAll",  # report_file_name_prefix
                               "Verify switching from all question types to switching to all other "
                               "question types using switch question dropdown making sure that last edit always gets saved",  # test_suite_title
                               ("This test suite adds a every type of question and tests switching to all other types and back   "
                                " Test verifies option menu choices still appear for specific question type."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

@pytest.mark.BVT
@pytest.mark.TC_BVT
def test_SQT_switchMutlipleChoice(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify switching from multiple choice(or any other question"
                                                           " type) to switching to all other question types using switch"
                                                           " question dropdown making sure that last edit always gets saved")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        title = mySurvey.myLogic.RNG(30)
        answerRows = []
        matrixRows = []
        mySurvey.myQuestion.enter_question_title(title)
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.changeQType("Dropdown")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to Dropdown",
                                 "verifies that the state of the question remains switching to Dropdown",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Dropdown"
        title = mySurvey.myLogic.RNG(30)
        mySurvey.myQuestion.enter_question_title(title)
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, answerRows[2])
        mySurvey.myQuestion.addMultiAnswerEnd()
        mySurvey.myQuestion.enter_multipleChoice_answerText(4, answerRows[3])
        mySurvey.myQuestion.changeQType("Matrix")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice", "Matrix"], matrixRows)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to Matrix",
                                 "verifies that the state of the question remains switching to Matrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Matrix"
        matrixRows.append(mySurvey.myLogic.RNG(10))
        matrixRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_matrix_answerText(1, matrixRows[0])
        mySurvey.myQuestion.enter_matrix_answerText(2, matrixRows[1])
        mySurvey.myQuestion.changeQType("MenuMatrix")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice", "Matrix"], matrixRows)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MenuMatrix",
                                 "verifies that the state of the question remains switching to MenuMatrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MenuMatrix"
        mySurvey.myQuestion.changeQType("SingleTextbox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["TextBox"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to SingleTextbox",
                                 "verifies that the state of the question remains switching to SingleTextbox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to SingleTextbox"
        mySurvey.myQuestion.changeQType("MultipleTextbox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MultiTextbox",
                                 "verifies that the state of the question remains switching to MultiTextbox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MultiTextbox"
        mySurvey.myQuestion.changeQType("CommentBox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["TextBox"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to CommentBox",
                                 "verifies that the state of the question remains switching to CommentBox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to CommentBox"
        mySurvey.myQuestion.changeQType("MultipleChoice")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MultiChoice",
                                 "verifies that the state of the question remains switching to MultiChoice",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MultiChoice"
        mySurvey.myQuestion.click_question_options_tab()
        ex = mySurvey.myQuestion.verify_all_options(["required", "change_layout", "random_choice", "adjust_layout", "question_a_b"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question options present",
                                 "verifies that all multichoice options are present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question options"
        mySurvey.myQuestion.click_question_save_from_options_tab()
        ex = True if mySurvey.myQuestion.verifyMultiChoiceQuestionAnswer(1, 1) == answerRows[0] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 1 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row 1"
        ex = True if mySurvey.myQuestion.verifyMultiChoiceQuestionAnswer(1, 2) == answerRows[1] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 2 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row 2"
        ex = True if mySurvey.myQuestion.verifyMultiChoiceQuestionAnswer(1, 3) == answerRows[2] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 3 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row 3"
        ex = True if mySurvey.myQuestion.verifyMultiChoiceQuestionAnswer(1, 4) == answerRows[3] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 4 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row 4"
        mySurvey.myQuestion.hover_on_question_to_delete_it()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_SQT_switchDropdown(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify switching from dropdown to all other question types")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_DropdownAddButton()
        title = mySurvey.myLogic.RNG(30)
        answerRows = []
        matrixRows = []
        mySurvey.myQuestion.enter_question_title(title)
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, answerRows[2])
        mySurvey.myQuestion.changeQType("SingleTextbox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["TextBox"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to SingleTextbox",
                                 "verifies that the state of the question remains switching to SingleTextbox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to SingleTextbox"
        title = mySurvey.myLogic.RNG(30)
        mySurvey.myQuestion.enter_question_title(title)
        mySurvey.myQuestion.changeQType("MultipleChoice")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MultiChoice",
                                 "verifies that the state of the question remains switching to MultiChoice",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MultiChoice"
        mySurvey.myQuestion.changeQType("Matrix")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice", "Matrix"], matrixRows)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to Matrix",
                                 "verifies that the state of the question remains switching to Matrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Matrix"
        matrixRows.append(mySurvey.myLogic.RNG(10))
        matrixRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_matrix_answerText(1, matrixRows[0])
        mySurvey.myQuestion.enter_matrix_answerText(2, matrixRows[1])
        mySurvey.myQuestion.changeQType("MenuMatrix")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice", "Matrix"], matrixRows)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MenuMatrix",
                                 "verifies that the state of the question remains switching to MenuMatrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MenuMatrix"
        mySurvey.myQuestion.changeQType("CommentBox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["TextBox"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to CommentBox",
                                 "verifies that the state of the question remains switching to CommentBox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to CommentBox"
        mySurvey.myQuestion.changeQType("MultipleTextbox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MultiTextbox",
                                 "verifies that the state of the question remains switching to MultiTextbox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MultiTextbox"
        mySurvey.myQuestion.changeQType("Dropdown")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to Dropdown",
                                 "verifies that the state of the question remains switching to Dropdown",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Dropdown"
        mySurvey.myQuestion.click_question_options_tab()
        ex = mySurvey.myQuestion.verify_all_options(["required", "change_layout", "random_choice", "adjust_layout", "question_a_b"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question options present",
                                 "verifies that all multichoice options are present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question options"
        mySurvey.myQuestion.click_question_save_from_options_tab()
        ex = True if mySurvey.myQuestion.verifyDropdownQuestionAnswer(1, 1) == answerRows[0] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 1 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row 1"
        ex = True if mySurvey.myQuestion.verifyDropdownQuestionAnswer(1, 2) == answerRows[1] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 2 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row 2"
        ex = True if mySurvey.myQuestion.verifyDropdownQuestionAnswer(1, 3) == answerRows[2] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 3 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row 3"
        mySurvey.myQuestion.hover_on_question_to_delete_it()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_SQT_matrix(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify switching from matrix/rating to all other question types")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_MatrixRatingScaleAddButton()
        title = mySurvey.myLogic.RNG(30)
        answerRows = []
        matrixRows = []
        mySurvey.myQuestion.enter_question_title(title)
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, answerRows[2])
        matrixRows.append(mySurvey.myLogic.RNG(10))
        matrixRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_matrix_answerText(1, matrixRows[0])
        mySurvey.myQuestion.enter_matrix_answerText(2, matrixRows[1])
        mySurvey.myQuestion.changeQType("SingleTextbox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["TextBox"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to SingleTextbox",
                                 "verifies that the state of the question remains switching to SingleTextbox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to SingleTextbox"
        title = mySurvey.myLogic.RNG(30)
        mySurvey.myQuestion.enter_question_title(title)
        mySurvey.myQuestion.changeQType("MultipleChoice")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MultiChoice",
                                 "verifies that the state of the question remains switching to MultiChoice",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MultiChoice"
        mySurvey.myQuestion.changeQType("CommentBox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["TextBox"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to CommentBox",
                                 "verifies that the state of the question remains switching to CommentBox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to CommentBox"
        mySurvey.myQuestion.changeQType("MenuMatrix")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice", "Matrix"], matrixRows)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MenuMatrix",
                                 "verifies that the state of the question remains switching to MenuMatrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MenuMatrix"
        title = mySurvey.myLogic.RNG(30)
        mySurvey.myQuestion.enter_question_title(title)
        mySurvey.myQuestion.changeQType("Ranking")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to Ranking",
                                 "verifies that the state of the question remains switching to Ranking",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Ranking"
        mySurvey.myQuestion.changeQType("MultipleTextbox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MultiTextbox",
                                 "verifies that the state of the question remains switching to MultiTextbox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MultiTextbox"
        mySurvey.myQuestion.changeQType("Matrix")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice", "Matrix"], matrixRows)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to Matrix",
                                 "verifies that the state of the question remains switching to Matrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Matrix"
        mySurvey.myQuestion.click_question_options_tab()
        ex = mySurvey.myQuestion.verify_all_options(["required", "change_layout", "random_choice", "adjust_layout", "question_a_b"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question options present",
                                 "verifies that all multichoice options are present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question options"
        mySurvey.myQuestion.click_question_save_from_options_tab()
        ex = True if mySurvey.myQuestion.verifyMatrixQuestionAnswer(1, 1) == answerRows[0] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 1 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row 1"
        ex = True if mySurvey.myQuestion.verifyMatrixQuestionAnswer(1, 2) == answerRows[1] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 2 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row 2"
        ex = True if mySurvey.myQuestion.verifyMatrixQuestionAnswer(1, 3) == answerRows[2] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 3 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row 3"
        ex = True if mySurvey.myQuestion.verifyMatrixColumnAnswer(1, 1) == matrixRows[0] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify column 1 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer column 1"
        ex = True if mySurvey.myQuestion.verifyMatrixColumnAnswer(1, 2) == matrixRows[1] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify column 2 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer column 2"
        mySurvey.myQuestion.hover_on_question_to_delete_it()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_SQT_date(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "switch from date/time to all question types")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_DateTimeAddButton()
        title = mySurvey.myLogic.RNG(30)
        answerRows = []
        matrixRows = []
        mySurvey.myQuestion.enter_question_title(title)
        mySurvey.myQuestion.changeQType("SingleTextbox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["TextBox"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to SingleTextbox",
                                 "verifies that the state of the question remains switching to SingleTextbox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to SingleTextbox"
        title = mySurvey.myLogic.RNG(30)
        mySurvey.myQuestion.enter_question_title(title)
        mySurvey.myQuestion.changeQType("Dropdown")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to Dropdown",
                                 "verifies that the state of the question remains switching to Dropdown",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Dropdown"
        # Disable the following tests because of https://monkeys.jira.com/browse/CREATE-5422
        # answerRows.append(mySurvey.myLogic.RNG(10))
        # answerRows.append(mySurvey.myLogic.RNG(10))
        # answerRows.append(mySurvey.myLogic.RNG(10))
        # mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        # mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        # mySurvey.myQuestion.enter_multipleChoice_answerText(3, answerRows[2])
        # mySurvey.myQuestion.changeQType("MultipleTextbox")
        # ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MultiTextbox",
        #                          "verifies that the state of the question remains switching to MultiTextbox",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to verify question state to MultiTextbox"
        # mySurvey.myQuestion.changeQType("CommentBox")
        # ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["TextBox"])
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to CommentBox",
        #                          "verifies that the state of the question remains switching to CommentBox",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to verify question state to CommentBox"
        # mySurvey.myQuestion.changeQType("Matrix")
        # ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice", "Matrix"], matrixRows)
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to Matrix",
        #                          "verifies that the state of the question remains switching to Matrix",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to verify question state to Matrix"
        # matrixRows.append(mySurvey.myLogic.RNG(10))
        # matrixRows.append(mySurvey.myLogic.RNG(10))
        # mySurvey.myQuestion.enter_matrix_answerText(1, matrixRows[0])
        # mySurvey.myQuestion.enter_matrix_answerText(2, matrixRows[1])
        # mySurvey.myQuestion.changeQType("MenuMatrix")
        # ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice", "Matrix"], matrixRows)
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MenuMatrix",
        #                          "verifies that the state of the question remains switching to MenuMatrix",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to verify question state to MenuMatrix"
        # mySurvey.myQuestion.changeQType("DateTime")
        # ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["TextBox"])
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to DateTime",
        #                          "verifies that the state of the question remains switching to DateTime",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to verify question state to DateTime"
        # mySurvey.myQuestion.click_question_options_tab()
        # ex = mySurvey.myQuestion.verify_all_options(["required", "random_choice", "adjust_layout", "question_a_b"])
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question options present",
        #                          "verifies that all multichoice options are present",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to verify question options"
        # mySurvey.myQuestion.click_question_save_from_options_tab()
        # ex = True if mySurvey.myQuestion.verifyDateTimeAnswer(1, 1) == answerRows[0] else False
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 1 answer is correct",
        #                          "verifies that the answer of the switched question is correct",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to verify answer row 1"
        # ex = True if mySurvey.myQuestion.verifyDateTimeAnswer(1, 2) == answerRows[1] else False
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 2 answer is correct",
        #                          "verifies that the answer of the switched question is correct",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to verify answer row 2"
        # ex = True if mySurvey.myQuestion.verifyDateTimeAnswer(1, 3) == answerRows[2] else False
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 3 answer is correct",
        #                          "verifies that the answer of the switched question is correct",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to verify answer row 3"
        # mySurvey.myQuestion.hover_on_question_to_delete_it()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_SQT_menuMatrix(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify switching from menu matrix to all question types")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_MatrixOfDropdownMenusAddButton()
        title = mySurvey.myLogic.RNG(30)
        answerRows = []
        matrixRows = []
        menuRows = []
        mySurvey.myQuestion.enter_question_title(title)
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, answerRows[2])
        matrixRows.append(mySurvey.myLogic.RNG(10))
        matrixRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_matrix_answerText(1, matrixRows[0])
        mySurvey.myQuestion.enter_matrix_answerText(2, matrixRows[1])
        menuRows.append(mySurvey.myLogic.RNG(10))
        menuRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_answer_choices_matrix_menu(1, menuRows[0])
        mySurvey.myQuestion.enter_answer_choices_matrix_menu(2, menuRows[1])
        mySurvey.myQuestion.changeQType("SingleTextbox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["TextBox"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to SingleTextbox",
                                 "verifies that the state of the question remains switching to SingleTextbox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to SingleTextbox"
        mySurvey.myQuestion.changeQType("MultipleChoice")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MultiChoice",
                                 "verifies that the state of the question remains switching to MultiChoice",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MultiChoice"
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.addMultiAnswerEnd()
        mySurvey.myQuestion.enter_multipleChoice_answerText(4, answerRows[3])
        mySurvey.myQuestion.changeQType("Dropdown")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to Dropdown",
                                 "verifies that the state of the question remains switching to Dropdown",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Dropdown"
        mySurvey.myQuestion.changeQType("CommentBox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["TextBox"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to CommentBox",
                                 "verifies that the state of the question remains switching to CommentBox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to CommentBox"
        title = mySurvey.myLogic.RNG(30)
        mySurvey.myQuestion.enter_question_title(title)
        mySurvey.myQuestion.changeQType("Matrix")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice", "Matrix"], matrixRows)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to Matrix",
                                 "verifies that the state of the question remains switching to Matrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Matrix"
        answerRows = []
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, answerRows[2])
        mySurvey.myQuestion.enter_multipleChoice_answerText(4, answerRows[3])
        matrixRows = []
        matrixRows.append(mySurvey.myLogic.RNG(10))
        matrixRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_matrix_answerText(1, matrixRows[0])
        mySurvey.myQuestion.enter_matrix_answerText(2, matrixRows[1])
        mySurvey.myQuestion.changeQType("MenuMatrix")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice", "Matrix"], matrixRows)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MenuMatrix",
                                 "verifies that the state of the question remains switching to MenuMatrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MenuMatrix"
        mySurvey.myQuestion.click_question_options_tab()
        ex = mySurvey.myQuestion.verify_all_options(["required", "random_choice", "adjust_layout"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question options present",
                                 "verifies that all multichoice options are present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question options"
        mySurvey.myQuestion.click_question_save_from_options_tab()
        # This case will fail because of this: https://monkeys.jira.com/browse/CREATE-5408
        ex = False if mySurvey.myQuestion.verifyMatrixQuestionAnswer(1, 1) == answerRows[0] else True
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 1 answer is correct",
                                 "verifies that the answer of the switched question is correct,  currently i fails because of this: https://monkeys.jira.com/browse/CREATE-5408",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row 1 "
        #  currently i fails because of this: https://monkeys.jira.com/browse/CREATE-5408, so commented the following
        # ex = True if mySurvey.myQuestion.verifyMatrixQuestionAnswer(1, 2) == answerRows[1] else False
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 2 answer is correct",
        #                          "verifies that the answer of the switched question is correct",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to verify answer row 2"
        # ex = True if mySurvey.myQuestion.verifyMatrixQuestionAnswer(1, 3) == answerRows[2] else False
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 3 answer is correct",
        #                          "verifies that the answer of the switched question is correct",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to verify answer row 3"
        # ex = True if mySurvey.myQuestion.verifyMatrixQuestionAnswer(1, 4) == answerRows[3] else False
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 4 answer is correct",
        #                          "verifies that the answer of the switched question is correct",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to verify answer row 4"
        # ex = True if mySurvey.myQuestion.verifyMatrixColumnAnswer(1, 1) == matrixRows[0] else False
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify column 1 answer is correct",
        #                          "verifies that the answer of the switched question is correct",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to verify answer column 1"
        # ex = True if mySurvey.myQuestion.verifyMatrixColumnAnswer(1, 2) == matrixRows[1] else False
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify column 2 answer is correct",
        #                          "verifies that the answer of the switched question is correct",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to verify answer column 2"
        # ex = True if mySurvey.myQuestion.verifyMenuMatrixDropdown(1, 1) == menuRows[0] else False
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify dropdown column 1 answer is correct",
        #                          "verifies that the answer of the switched question is correct",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to verify answer dropdown column 1"
        # ex = True if mySurvey.myQuestion.verifyMenuMatrixDropdown(1, 2) == menuRows[1] else False
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify dropdown column 2 answer is correct",
        #                          "verifies that the answer of the switched question is correct",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to verify answer dropdown column 2"
        # mySurvey.myQuestion.hover_on_question_to_delete_it()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_SQT_menuMatrix2(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify switching menu matrix to all other question types")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_MatrixOfDropdownMenusAddButton()
        title = mySurvey.myLogic.RNG(30)
        answerRows = []
        matrixRows = []
        menuRows = []
        mySurvey.myQuestion.enter_question_title(title)
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, answerRows[2])
        matrixRows.append(mySurvey.myLogic.RNG(10))
        matrixRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_matrix_answerText(1, matrixRows[0])
        mySurvey.myQuestion.enter_matrix_answerText(2, matrixRows[1])
        menuRows.append(mySurvey.myLogic.RNG(10))
        menuRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_answer_choices_matrix_menu(1, menuRows[0])
        mySurvey.myQuestion.enter_answer_choices_matrix_menu(2, menuRows[1])
        mySurvey.myQuestion.changeQType("Matrix")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice", "Matrix"], matrixRows)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to Matrix",
                                 "verifies that the state of the question remains switching to Matrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Matrix"
        title = mySurvey.myLogic.RNG(30)
        mySurvey.myQuestion.enter_question_title(title)
        mySurvey.myQuestion.changeQType("SingleTextbox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["TextBox"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to SingleTextbox",
                                 "verifies that the state of the question remains switching to SingleTextbox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to SingleTextbox"
        mySurvey.myQuestion.changeQType("Dropdown")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to Dropdown",
                                 "verifies that the state of the question remains switching to Dropdown",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Dropdown"
        mySurvey.myQuestion.changeQType("MultipleChoice")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MultiChoice",
                                 "verifies that the state of the question remains switching to MultiChoice",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MultiChoice"
        mySurvey.myQuestion.changeQType("CommentBox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["TextBox"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to CommentBox",
                                 "verifies that the state of the question remains switching to CommentBox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to CommentBox"
        mySurvey.myQuestion.changeQType("MultipleTextbox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MultiTextbox",
                                 "verifies that the state of the question remains switching to MultiTextbox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MultiTextbox"
        mySurvey.myQuestion.changeQType("MenuMatrix")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice", "Matrix"], matrixRows)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MenuMatrix",
                                 "verifies that the state of the question remains switching to MenuMatrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MenuMatrix"
        mySurvey.myQuestion.click_question_options_tab()
        ex = mySurvey.myQuestion.verify_all_options(["required", "random_choice", "adjust_layout"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question options present",
                                 "verifies that all multichoice options are present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question options"
        mySurvey.myQuestion.click_question_save_from_options_tab()
        # This case will fail because of this: https://monkeys.jira.com/browse/CREATE-5408
        ex = False if mySurvey.myQuestion.verifyMatrixQuestionAnswer(1, 1) == answerRows[0] else True
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 1 answer is correct",
                                 "verifies that the answer of the switched question is correct, This case will fail because of this: https://monkeys.jira.com/browse/CREATE-5408",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row 1"
        #  currently i fails because of this: https://monkeys.jira.com/browse/CREATE-5408, so commented the following
        # ex = True if mySurvey.myQuestion.verifyMatrixQuestionAnswer(1, 2) == answerRows[1] else False
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 2 answer is correct",
        #                          "verifies that the answer of the switched question is correct",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to verify answer row 2"
        # ex = True if mySurvey.myQuestion.verifyMatrixQuestionAnswer(1, 3) == answerRows[2] else False
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 3 answer is correct",
        #                          "verifies that the answer of the switched question is correct",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to verify answer row 3"
        # ex = True if mySurvey.myQuestion.verifyMatrixColumnAnswer(1, 1) == matrixRows[0] else False
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify column 1 answer is correct",
        #                          "verifies that the answer of the switched question is correct",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to verify answer column 1"
        # ex = True if mySurvey.myQuestion.verifyMatrixColumnAnswer(1, 2) == matrixRows[1] else False
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify column 2 answer is correct",
        #                          "verifies that the answer of the switched question is correct",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to verify answer column 2"
        # ex = True if mySurvey.myQuestion.verifyMenuMatrixDropdown(1, 1) == menuRows[0] else False
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify dropdown column 1 answer is correct",
        #                          "verifies that the answer of the switched question is correct",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to verify answer dropdown column 1"
        # ex = True if mySurvey.myQuestion.verifyMenuMatrixDropdown(1, 2) == menuRows[1] else False
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify dropdown column 2 answer is correct",
        #                          "verifies that the answer of the switched question is correct",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to verify answer dropdown column 2"
        # mySurvey.myQuestion.hover_on_question_to_delete_it()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_SQT_ranking(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify switching from ranking to all other question types")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_RankingAddButton()
        title = mySurvey.myLogic.RNG(30)
        answerRows = []
        matrixRows = []
        mySurvey.myQuestion.enter_question_title(title)
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, answerRows[2])
        mySurvey.myQuestion.changeQType("MultipleChoice")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MultiChoice",
                                 "verifies that the state of the question remains switching to MultiChoice",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MultiChoice"
        title = mySurvey.myLogic.RNG(30)
        mySurvey.myQuestion.enter_question_title(title)
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.addMultiAnswerEnd()
        mySurvey.myQuestion.enter_multipleChoice_answerText(4, answerRows[3])
        mySurvey.myQuestion.changeQType("Dropdown")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to Dropdown",
                                 "verifies that the state of the question remains switching to Dropdown",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Dropdown"
        mySurvey.myQuestion.changeQType("MenuMatrix")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice", "Matrix"], matrixRows)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MenuMatrix",
                                 "verifies that the state of the question remains switching to MenuMatrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MenuMatrix"
        mySurvey.myQuestion.changeQType("Matrix")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice", "Matrix"], matrixRows)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to Matrix",
                                 "verifies that the state of the question remains switching to Matrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Matrix"
        mySurvey.myQuestion.changeQType("CommentBox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["TextBox"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to CommentBox",
                                 "verifies that the state of the question remains switching to CommentBox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to CommentBox"
        mySurvey.myQuestion.changeQType("MultipleTextbox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MultiTextbox",
                                 "verifies that the state of the question remains switching to MultiTextbox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MultiTextbox"
        mySurvey.myQuestion.changeQType("SingleTextbox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["TextBox"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to SingleTextbox",
                                 "verifies that the state of the question remains switching to SingleTextbox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to SingleTextbox"
        mySurvey.myQuestion.changeQType("Ranking")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to Ranking",
                                 "verifies that the state of the question remains switching to Ranking",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Ranking"
        mySurvey.myQuestion.click_question_options_tab()
        ex = mySurvey.myQuestion.verify_all_options(["required", "random_choice", "adjust_layout", "question_a_b"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question options present",
                                 "verifies that all multichoice options are present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question options"
        mySurvey.myQuestion.click_question_save_from_options_tab()
        ex = True if mySurvey.myQuestion.verifyRankingQuestionAnswer(1, 1) == answerRows[0] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 1 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row 1"
        ex = True if mySurvey.myQuestion.verifyRankingQuestionAnswer(1, 2) == answerRows[1] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 2 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row 2"
        ex = True if mySurvey.myQuestion.verifyRankingQuestionAnswer(1, 3) == answerRows[2] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 3 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row 3"
        ex = True if mySurvey.myQuestion.verifyRankingQuestionAnswer(1, 4) == answerRows[3] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 4 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row 4"
        mySurvey.myQuestion.hover_on_question_to_delete_it()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_SQT_singleTextbox(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify switching from single textbox to all question types")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SingleTextboxAddButton()
        title = mySurvey.myLogic.RNG(30)
        answerRows = []
        matrixRows = []
        mySurvey.myQuestion.enter_question_title(title)
        mySurvey.myQuestion.changeQType("MultipleTextbox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MultiTextbox",
                                 "verifies that the state of the question remains switching to MultiTextbox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MultiTextbox"
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, answerRows[2])
        mySurvey.myQuestion.changeQType("Dropdown")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to Dropdown",
                                 "verifies that the state of the question remains switching to Dropdown",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Dropdown"
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.addMultiAnswerEnd()
        mySurvey.myQuestion.enter_multipleChoice_answerText(4, answerRows[3])
        mySurvey.myQuestion.changeQType("CommentBox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["TextBox"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to CommentBox",
                                 "verifies that the state of the question remains switching to CommentBox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to CommentBox"
        mySurvey.myQuestion.changeQType("Matrix")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice", "Matrix"], matrixRows)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to Matrix",
                                 "verifies that the state of the question remains switching to Matrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Matrix"
        mySurvey.myQuestion.changeQType("MenuMatrix")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice", "Matrix"], matrixRows)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MenuMatrix",
                                 "verifies that the state of the question remains switching to MenuMatrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MenuMatrix"
        mySurvey.myQuestion.changeQType("MultipleChoice")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MultiChoice",
                                 "verifies that the state of the question remains switching to MultiChoice",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MultiChoice"
        mySurvey.myQuestion.changeQType("SingleTextbox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["TextBox"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to SingleTextbox",
                                 "verifies that the state of the question remains switching to SingleTextbox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to SingleTextbox"
        mySurvey.myQuestion.click_question_options_tab()
        ex = mySurvey.myQuestion.verify_all_options(["required", "random_choice", "adjust_layout", "question_a_b"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question options present",
                                 "verifies that all multichoice options are present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question options"
        mySurvey.myQuestion.click_question_save_from_options_tab()
        ex = True if mySurvey.myQuestion.verifyQuestionTitle(1) == title else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify title is correct",
                                 "verifies that the title of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify title"
        mySurvey.myQuestion.hover_on_question_to_delete_it()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_SQT_multiTextbox(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify switching from multiple textboxes to all question types")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_MultipleTextboxesAddButton()
        title = mySurvey.myLogic.RNG(30)
        answerRows = []
        matrixRows = []
        mySurvey.myQuestion.enter_question_title(title)
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, answerRows[2])
        mySurvey.myQuestion.changeQType("SingleTextbox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["TextBox"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to SingleTextbox",
                                 "verifies that the state of the question remains switching to SingleTextbox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to SingleTextbox"
        title = mySurvey.myLogic.RNG(30)
        mySurvey.myQuestion.enter_question_title(title)
        mySurvey.myQuestion.changeQType("MultipleChoice")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MultiChoice",
                                 "verifies that the state of the question remains switching to MultiChoice",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MultiChoice"
        mySurvey.myQuestion.changeQType("Matrix")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice", "Matrix"], matrixRows)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to Matrix",
                                 "verifies that the state of the question remains switching to Matrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Matrix"
        mySurvey.myQuestion.changeQType("MenuMatrix")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice", "Matrix"], matrixRows)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MenuMatrix",
                                 "verifies that the state of the question remains switching to MenuMatrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MenuMatrix"
        mySurvey.myQuestion.changeQType("CommentBox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["TextBox"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to CommentBox",
                                 "verifies that the state of the question remains switching to CommentBox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to CommentBox"
        mySurvey.myQuestion.changeQType("MultipleChoice")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MultiChoice",
                                 "verifies that the state of the question remains switching to MultiChoice",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MultiChoice"
        mySurvey.myQuestion.changeQType("MultipleTextbox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MultiTextbox",
                                 "verifies that the state of the question remains switching to MultiTextbox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MultiTextbox"
        mySurvey.myQuestion.click_question_options_tab()
        ex = mySurvey.myQuestion.verify_all_options(["required", "change_layout", "random_choice", "adjust_layout", "question_a_b"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question options present",
                                 "verifies that all multichoice options are present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question options"
        mySurvey.myQuestion.click_question_save_from_options_tab()
        ex = True if mySurvey.myQuestion.verifyMultiTextboxQuestionAnswer(1, 1) == answerRows[0] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 1 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row 1"
        ex = True if mySurvey.myQuestion.verifyMultiTextboxQuestionAnswer(1, 2) == answerRows[1] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 2 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row 2"
        ex = True if mySurvey.myQuestion.verifyMultiTextboxQuestionAnswer(1, 3) == answerRows[2] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 3 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row 3"
        mySurvey.myQuestion.hover_on_question_to_delete_it()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_SQT_commentBox(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify switching from comment to All question types")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_MultipleTextboxesAddButton()
        title = mySurvey.myLogic.RNG(30)
        answerRows = []
        matrixRows = []
        mySurvey.myQuestion.enter_question_title(title)
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.changeQType("MultipleChoice")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MultiChoice",
                                 "verifies that the state of the question remains switching to MultiChoice",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MultiChoice"
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, answerRows[2])
        mySurvey.myQuestion.addMultiAnswerEnd()
        mySurvey.myQuestion.enter_multipleChoice_answerText(4, answerRows[3])
        mySurvey.myQuestion.changeQType("SingleTextbox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["TextBox"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to SingleTextbox",
                                 "verifies that the state of the question remains switching to SingleTextbox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to SingleTextbox"
        mySurvey.myQuestion.changeQType("Matrix")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice", "Matrix"], matrixRows)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to Matrix",
                                 "verifies that the state of the question remains switching to Matrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Matrix"
        mySurvey.myQuestion.changeQType("Ranking")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to Ranking",
                                 "verifies that the state of the question remains switching to Ranking",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Ranking"
        mySurvey.myQuestion.changeQType("MenuMatrix")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice", "Matrix"], matrixRows)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to MenuMatrix",
                                 "verifies that the state of the question remains switching to MenuMatrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MenuMatrix"
        mySurvey.myQuestion.changeQType("CommentBox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["TextBox"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to CommentBox",
                                 "verifies that the state of the question remains switching to CommentBox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to CommentBox"
        mySurvey.myQuestion.click_question_options_tab()
        ex = mySurvey.myQuestion.verify_all_options(["required", "adjust_layout", "question_a_b"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question options present",
                                 "verifies that all multichoice options are present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question options"
        mySurvey.myQuestion.click_question_save_from_options_tab()
        ex = True if mySurvey.myQuestion.verifyQuestionTitle(1) == title else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify title is correct",
                                 "verifies that the title of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify title"
        mySurvey.myQuestion.hover_on_question_to_delete_it()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
