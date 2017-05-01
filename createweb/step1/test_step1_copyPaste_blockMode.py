from smsdk.qafw.create.create_utils import reporting_wrapper, get_env_data
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest
from smsdk.qafw.create.create_start_new import NewSurvey

questions=[
    dict(title="Favorite Akizuki Class", answers=["Akizuki", "Teruzuki", "Hatsuzuki"], qType="multipleChoice"),
    dict(title="Favorite Shiratsuyu Class", answers=["Yuudachi", "Shigure", "Harusame", "Kawakaze"], qType="multipleChoice"),
    dict(title="Favorite Sendai Class", answers=["Naka", "Sendai", "Jintsuu"], qType="multipleChoice"),
    dict(title="Favorite Myoukou Class", answers=["Myoukou", "Ashigara", "Haguro", "Nachi"], qType="multipleChoice"),
    dict(title="Best Kongou Class", answers=["Kongou", "Haruna", "Kirishima", "Hiei"], qType="multipleChoice"),
    dict(title="Best Nagato Class", answers=["Nagato", "Mutsu"], qType="multipleChoice"),
    dict(title="Best Mogami Class", answers=["Mogami", "Suzuya", "Kumano", "Mikuma"], qType="multipleChoice"),
    dict(title="Favorite Akatsuki Class", answers=["Akatsuki", "Hibiki", "Inazuma", "Ikazuchi"], qType="multipleChoice"),
    dict(title="Poi?", answers=None, qType="TextBox"),
    dict(title="Nanodesu?", answers=None, qType="TextBox")
]



@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestStep1CopyPasteBlockMode/",  # report_relative_location
                               "test_step1_copyPaste_blockMode",  # report_file_name_prefix
                               "Test creating new survey via step1 copyPaste in BLOCK MODE",  # test_suite_title
                               ("Test to make sure step 1 survey creation functions with copyPaste IN BLOCK MODE"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_step1_blockMode(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "test_step1_blockMode")
    try:

        mySurvey.myCreate.click_new_survey()
        step1 = NewSurvey(driver)
        step1.create_survey_from_scratch()
        surveyTitle = 'test_' + mySurvey.myLogic.RNG(40)
        step1.enter_survey_title(surveyTitle)
        mySurvey.myCreate.check_step1_copyPaste_function()
        step1.click_lets_go_new()
        mySurvey.myCreate.input_step1_draftMode_text()
        ex = mySurvey.myCreate.verify_survey_title(surveyTitle)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify step 1 Survey Creation",
                                     "verifies that survey title matches step 1 input.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
        assert ex, "Failed to verify step 1 survey Creations"
        for x in xrange(10):
            mySurvey.myQuestion.click_on_question_to_edit(x+1)
            ex = mySurvey.myQuestion.verifyQuestionSwitchState(questions[x]["title"], questions[x]["answers"], [questions[x]["qType"]])
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question added from copyPaste draft mode",
                                 "verifies that the state of the question was copyPasted correctly",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
            assert ex, "Failed to verify question state for question " + str(x+1)
            mySurvey.myQuestion.click_question_save_from_edit_tab()
            ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 10)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Save question type",
                                     "Verified that question saved to survey",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify question saved to survey."
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myQuestion.changeQType("Matrix")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myDesign.scroll_to_top()
        mySurvey.myOptions.unfold_OptionsRegion()
        mySurvey.myDesign.click_add_logo()
        mySurvey.myDesign.click_upload_logo()
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myOptions.unfold_OptionsRegion()
        mySurvey.myOptions.toggle_progressBar()
        ex = mySurvey.myTheme.verifyThemeApplied("Sky")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Sky Theme",
                                 "Compares current theme with values of what the theme should have",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Sky Theme " + str(ex)

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_step1_blockMode_switchMutlipleChoice(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify switching from multiple choice(or any other question"
                                                           " type) to switching to all other question types using switch"
                                                           " question dropdown making sure that last edit always gets saved")
    try:

        mySurvey.myCreate.click_new_survey()
        step1 = NewSurvey(driver)
        step1.create_survey_from_scratch()
        surveyTitle = 'test_' + mySurvey.myLogic.RNG(40)
        step1.enter_survey_title(surveyTitle)
        mySurvey.myCreate.check_step1_copyPaste_function()
        step1.click_lets_go_new()
        mySurvey.myCreate.input_step1_draftMode_text(payload="""
            Favorite Kuma Class
            Kuma
            Tama
            Kitakami
            Ooi
            Kiso
        """)
        title = "Favorite Kuma Class"
        answerRows = ["Kuma", "Tama", "Kitakami", "Ooi", "Kiso"]
        matrixRows = []
        ex = mySurvey.myCreate.verify_survey_title(surveyTitle)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify step 1 Survey Creation",
                                     "verifies that survey title matches step 1 input.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
        assert ex, "Failed to verify step 1 survey Creations"
        mySurvey.myQuestion.click_on_question_to_edit()
        mySurvey.myQuestion.changeQType("Dropdown")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to Dropdown",
                                 "verifies that the state of the question remains switching to Dropdown",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Dropdown"
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
        mySurvey.myQuestion.click_question_save_from_edit_tab()
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


def test_step1_blockMode_singleTextbox(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify switching from single textbox to all question types")
    try:
        mySurvey.myCreate.click_new_survey()
        step1 = NewSurvey(driver)
        step1.create_survey_from_scratch()
        surveyTitle = 'test_' + mySurvey.myLogic.RNG(40)
        step1.enter_survey_title(surveyTitle)
        mySurvey.myCreate.check_step1_copyPaste_function()
        step1.click_lets_go_new()
        mySurvey.myCreate.input_step1_draftMode_text(payload="""
            Poi!
        """)
        title = "Poi!"
        answerRows = []
        matrixRows = []
        ex = mySurvey.myCreate.verify_survey_title(surveyTitle)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify step 1 Survey Creation",
                                     "verifies that survey title matches step 1 input.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
        assert ex, "Failed to verify step 1 survey Creations"
        mySurvey.myQuestion.click_on_question_to_edit()
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
        mySurvey.myQuestion.click_question_save_from_edit_tab()
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


@pytest.mark.skipif(True, reason="skip this test as new copy & paste questions window do not have the learn more "
                                 "and skip page links")
def test_step1_blockMode_skip(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "test_step1_blockMode_skip")
    try:
        surveyTitle = "Survey Title"
        domain = get_env_data()['domain']
        driver.get("{}/create/draft/?mode=block".format(domain))
        ex = mySurvey.myCreate.verify_step1_learnMore()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify step 1 copyPaste help",
                                     "verifies that learnmore button driects to copyPaste help page.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
        assert ex, "Failed to verify copyPaste Learn More"
        mySurvey.myCreate.skip_step1_copyPaste()
        ex = mySurvey.myCreate.verify_survey_title(surveyTitle)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify step 1 Survey Creation",
                                     "verifies that survey title matches step 1 input.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
        assert ex, "Failed to verify step 1 survey Creations"
        ex = True if mySurvey.myCreate.num_questions_in_survey() == 0 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify skipped copyPaste in step1",
                                     "verifies that no questions added via copyPaste feature.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
        assert ex, "Failed to verify skipping step1 copyPaste Feature"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_step1_blockMode_largeLoad(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "test_step1_blockMode_largeLoad")
    try:
        mySurvey.myCreate.click_new_survey()
        step1 = NewSurvey(driver)
        step1.create_survey_from_scratch()
        surveyTitle = 'test_' + mySurvey.myLogic.RNG(40)
        step1.enter_survey_title(surveyTitle)
        mySurvey.myCreate.check_step1_copyPaste_function()
        step1.click_lets_go_new()
        largeLoad = "1" +'\n\n'
        for x in xrange(99):
            largeLoad += str(x+2) + '\n\n'
        mySurvey.myCreate.input_step1_draftMode_text(payload=largeLoad, textWrap=True)
        ex = mySurvey.myCreate.verify_survey_title(surveyTitle)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify step 1 Survey Creation",
                                     "verifies that survey title matches step 1 input.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
        assert ex, "Failed to verify step 1 survey Creations"
        mySurvey.myCreate.wait_until_n_question_added(100)
        ex = True if mySurvey.myCreate.num_questions_in_survey() == 100 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify all questions added to survey",
                                     "verifies that all questions added via copyPaste feature.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
        assert ex, "Failed to verify adding step1 copyPaste Feature"
        ex = True if mySurvey.myCreate.num_questions_in_page(1) == 100 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify 100 questions on page 1",
                                     "verifies that only 100 questions added to page 1.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
        assert ex, "Failed to verify 100 questions added to page 1"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()