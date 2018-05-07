from tests.python.lib.create.create_utils import get_testrail_info
from smlib.qautils.reporting.report_message_types import ReportMessageTypes
import traceback
import pytest


@pytest.mark.DESIGN
def test_design_addNewQuestion_default(request, create_survey):
    driver, mySurvey, report = create_survey
    testcasename = request.node.nodeid
    logging_dict = get_testrail_info(testcasename)
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button.",
                             logging_dict=logging_dict)
    try:
        mySurvey.myCreate.create_first_question_from_live_preview("MultipleChoice")
        ex = "question-single-choice-radio" in mySurvey.myQuestion.get_question_type_of_current_editing()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is multiple choice",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify newly added question."
        mySurvey.myQuestion.enter_question_title('multiple choice')
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "1")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "2")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add MultipleChoice question type to survey ",
                                 "Verified that MultipleChoice question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add MultipleChoice question to survey."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.DESIGN
def test_design_addNewQuestion_multipleChoice(request, create_survey):
    driver, mySurvey, report = create_survey
    testcasename = request.node.nodeid
    logging_dict = get_testrail_info(testcasename)
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (MultiChoice).",
                             logging_dict=logging_dict)
    try:
        mySurvey.myCreate.create_first_question_from_live_preview("MultipleChoice")
        ex = "question-single-choice-radio" in mySurvey.myQuestion.get_question_type_of_current_editing()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is multiple choice",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify newly added question."
        mySurvey.myQuestion.enter_question_title('multiple choice')
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "1")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "2")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add MultipleChoice question type to survey ",
                                 "Verified that MultipleChoice question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add MultipleChoice question to survey."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.DESIGN
def test_design_addNewQuestion_dropdown(request, create_survey):
    driver, mySurvey, report = create_survey
    testcasename = request.node.nodeid
    logging_dict = get_testrail_info(testcasename)
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (Dropdown).",
                             logging_dict=logging_dict)
    try:
        mySurvey.myCreate.create_first_question_from_live_preview("Dropdown")
        ex = "question-single-choice-select" in mySurvey.myQuestion.get_question_type_of_current_editing()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is dropdown",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify newly added question."
        mySurvey.myQuestion.enter_question_title('dropdown choice')
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "1")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "2")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add dropdown question type to survey ",
                                 "Verified that dropdown question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add dropdown question to survey."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.DESIGN
def test_design_addNewQuestion_matrix(request, create_survey):
    driver, mySurvey, report = create_survey
    testcasename = request.node.nodeid
    logging_dict = get_testrail_info(testcasename)
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (Matrix).",
                             logging_dict=logging_dict)
    try:
        mySurvey.myCreate.create_first_question_from_live_preview("Matrix")
        ex = "question-matrix" in mySurvey.myQuestion.get_question_type_of_current_editing()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is matrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify newly added question."
        mySurvey.myQuestion.enter_question_title('Matrix Rating Scale Question')
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "1")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "2")
        mySurvey.myQuestion.enter_matrix_answerText(1, "A")
        mySurvey.myQuestion.enter_matrix_answerText(2, "B")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Matrix Rating Scale question type to survey ",
                                 "Verified that Matrix Rating Scale question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add Matrix question to survey."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.DESIGN
def test_design_addNewQuestion_menuMatrix(request, create_survey):
    driver, mySurvey, report = create_survey
    testcasename = request.node.nodeid
    logging_dict = get_testrail_info(testcasename)
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (Menu Matrix).",
                             logging_dict=logging_dict)
    try:
        mySurvey.myCreate.create_first_question_from_live_preview("MenuMatrix")
        ex = "question-menu-matrix" in mySurvey.myQuestion.get_question_type_of_current_editing()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is menu matrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify newly added question."
        mySurvey.myQuestion.enter_question_title('Matrix of Dropdown Menus Question')
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "1")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "2")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "3")
        mySurvey.myQuestion.enter_matrix_answerText(1, "1")
        mySurvey.myQuestion.enter_matrix_answerText(2, "2")
        mySurvey.myQuestion.enter_answer_choices_matrix_menu(1, "1")
        mySurvey.myQuestion.enter_answer_choices_matrix_menu(2, "2")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Matrix of Dropdown Menus question type to survey ",
                                 "Verified that Matrix of Dropdown Menus question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add Matrix of Dropdown Menus question to survey."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.DESIGN
def test_design_addNewQuestion_ranking(request, create_survey):
    driver, mySurvey, report = create_survey
    testcasename = request.node.nodeid
    logging_dict = get_testrail_info(testcasename)
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (Ranking).",
                             logging_dict=logging_dict)
    try:
        mySurvey.myCreate.create_first_question_from_live_preview("Ranking")
        ex = "question-ranking" in mySurvey.myQuestion.get_question_type_of_current_editing()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is matrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify newly added question."
        mySurvey.myQuestion.enter_question_title('Ranking Question')
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "R1")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "R2")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Ranking question type to survey ",
                                 "Verified that Ranking question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add Ranking question to survey."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.DESIGN
def test_design_addNewQuestion_NPS(request, create_survey):
    driver, mySurvey, report = create_survey
    testcasename = request.node.nodeid
    logging_dict = get_testrail_info(testcasename)
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (NPS).",
                             logging_dict=logging_dict)
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NetPromoterScoreAddButton()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myQuestion.hover_on_question(1)
        ex = True if mySurvey.myBank.verifyCertIcon("SurveyMonkey") else False
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is NPS",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify newly added question."

        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add NPS question type to survey ",
                                 "Verified that NPS question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add NPS question to survey."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.DESIGN
def test_design_addNewQuestion_singleTextbox(request, create_survey):
    driver, mySurvey, report = create_survey
    testcasename = request.node.nodeid
    logging_dict = get_testrail_info(testcasename)
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (Single Textbox).",
                             logging_dict=logging_dict)
    try:
        mySurvey.myCreate.create_first_question_from_live_preview("SingleTextbox")
        ex = "question-open-ended-single" in mySurvey.myQuestion.get_question_type_of_current_editing()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is Single Textbox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify newly added question."
        mySurvey.myQuestion.enter_question_title('SingleTextbox')
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add SingleTextbox question type to survey ",
                                 "Verified that SingleTextbox question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add SingleTextbox question to survey."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.DESIGN
def test_design_addNewQuestion_multiTextbox(request, create_survey):
    driver, mySurvey, report = create_survey
    testcasename = request.node.nodeid
    logging_dict = get_testrail_info(testcasename)
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (Multi Textbox).",
                             logging_dict=logging_dict)
    try:
        mySurvey.myCreate.create_first_question_from_live_preview("MultipleTextbox")
        ex = "question-open-ended-multi" in mySurvey.myQuestion.get_question_type_of_current_editing()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is Multiple Textboxes",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify newly added question."
        mySurvey.myQuestion.enter_question_title('Multiple Textbox Question')
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "1")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "2")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "3")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Multiple Textbox question type to survey ",
                                 "Verified that Multiple Textbox question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add Multiple Textbox question to survey."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.DESIGN
def test_design_addNewQuestion_commentBox(request, create_survey):
    driver, mySurvey, report = create_survey
    testcasename = request.node.nodeid
    logging_dict = get_testrail_info(testcasename)
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (Comment Box).",
                             logging_dict=logging_dict)
    try:
        mySurvey.myCreate.create_first_question_from_live_preview("CommentBox")
        ex = "question-essay" in mySurvey.myQuestion.get_question_type_of_current_editing()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is Comment Box",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify newly added question."
        mySurvey.myQuestion.enter_question_title('CommentBox Question')
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add CommentBox question type to survey ",
                                 "Verified that CommentBox question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add CommentBox question to survey."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.DESIGN
def test_design_addNewQuestion_contactInfo(request, create_survey):
    driver, mySurvey, report = create_survey
    testcasename = request.node.nodeid
    logging_dict = get_testrail_info(testcasename)
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (Contact Info).",
                             logging_dict=logging_dict)
    try:
        mySurvey.myCreate.create_first_question_from_live_preview("ContactInfo")
        ex = "question-demographic" in mySurvey.myQuestion.get_question_type_of_current_editing()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is Contact Info",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify newly added question."
        mySurvey.myQuestion.enter_question_title('Contact Information Question')
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Contact Information question type to survey ",
                                 "Verified that Contact Information question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add Contact Information question to survey."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.DESIGN
def test_design_addNewQuestion_dateTime(request, create_survey):
    driver, mySurvey, report = create_survey
    testcasename = request.node.nodeid
    logging_dict = get_testrail_info(testcasename)
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (DateTime).",
                             logging_dict=logging_dict)
    try:
        mySurvey.myCreate.create_first_question_from_live_preview("DateTime")
        ex = "question-datetime" in mySurvey.myQuestion.get_question_type_of_current_editing()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is Date Time",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify newly added question."
        mySurvey.myQuestion.enter_question_title('Date Time Question')
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Date Time question type to survey ",
                                 "Verified that Date Time question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add Date Time question to survey."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.DESIGN
def test_design_addFileupload(request, create_survey):
    driver, mySurvey, report = create_survey
    testcasename = request.node.nodeid
    logging_dict = get_testrail_info(testcasename)
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (Text).",
                             logging_dict=logging_dict)
    try:
        mySurvey.myCreate.create_first_question_from_live_preview("FileUpload")
        mySurvey.myQuestion.enter_question_title('FileUpload')
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add FileUpload question type to survey ",
                                 "Verified that FileUpload question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add FileUpload question to survey."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

@pytest.mark.DESIGN
def test_design_addNewQuestion_text(request, create_survey):
    driver, mySurvey, report = create_survey
    testcasename = request.node.nodeid
    logging_dict = get_testrail_info(testcasename)
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (Text).",
                             logging_dict=logging_dict)
    try:
        mySurvey.myBuilder.unfold_BuilderRegion
        mySurvey.myBuilder.click_TextAddButton()
        ex = "question-presentation-text" in mySurvey.myQuestion.get_question_type_of_current_editing()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is Text",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify newly added question."

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.DESIGN
def test_design_addNewQuestion_Image(request, create_survey):
    driver, mySurvey, report = create_survey
    testcasename = request.node.nodeid
    logging_dict = get_testrail_info(testcasename)
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (Image).",
                             logging_dict=logging_dict)
    try:
        mySurvey.myBuilder.unfold_BuilderRegion
        mySurvey.myBuilder.click_ImageAddButton()
        ex = "question-presentation-image" in mySurvey.myQuestion.get_question_type_of_current_editing()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is Image",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify newly added question."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.DESIGN
def test_design_addNewQuestion_textAB(request, create_survey):
    driver, mySurvey, report = create_survey
    testcasename = request.node.nodeid
    logging_dict = get_testrail_info(testcasename)
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (TextAB).",
                             logging_dict=logging_dict)
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_TextABTestAddButton()
        question_class = mySurvey.myQuestion.get_question_type_of_current_editing()
        ex = 'question-presentation-text' in question_class and 'random-assignment' in question_class
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is Text AB",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify newly added question."
        mySurvey.myQuestion.enterTextABTestVar("sush", 1)
        mySurvey.myQuestion.enterTextABTestVar("monk!", 2)
        mySurvey.myQuestion.addNewTextABTestVar("root?")
        mySurvey.myQuestion.addNewTextABTestVar("thanks!")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Date Time question type to survey ",
                                 "Verified that Date Time question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add Date Time question to survey."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.DESIGN
def test_design_addNewQuestion_imageAB(request, create_survey):
    driver, mySurvey, report = create_survey
    testcasename = request.node.nodeid
    logging_dict = get_testrail_info(testcasename)
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (ImageAB).",
                             logging_dict=logging_dict)
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_ImageABTestAddButton()
        ex = 'question-presentation-image' in mySurvey.myQuestion.get_question_type_of_current_editing()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is Image AB",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify newly added question."
        mySurvey.myQuestion.enter_imageAB_label(1, "Image AB Title A")
        mySurvey.myQuestion.enter_imageAB_url(1,
                                               "http://images5.fanpop.com/image/photos/31100000/"
                                               "Keep-Calm-and-Continue-Testing-portal-2-31140076-453-700.jpg")
        mySurvey.myQuestion.enter_imageAB_label(2, "Image AB Title B")  # First curly brace gets eaten by webdriver
        mySurvey.myQuestion.enter_imageAB_url(2,
                                               "http://images4.fanpop.com/image/photos/21200000"
                                               "/TACOS-gir-21208550-838-953.jpg")
   
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify image ab question Add to Live Preview",
                                 "Verifies that image ab question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify image ab question added to live preview."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
