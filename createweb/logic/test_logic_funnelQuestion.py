from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicFunnelQuestion/",  # report_relative_location
                               "test_logic_funnelQuestion",  # report_file_name_prefix
                               "Basic funneling automation tests",  # test_suite_title
                               ("This test adds a sender and receiver question and funnels accordingly."
                                " Test then attempts attempts basic verification tests."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_funnelQuestion_senderAfterReceiver(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test funneling when receiver before sender.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best German Kanmusu?", 1,
                                                          ["Graf Zeppelin", "Bismarck", "Prinz Eugen", "U-511"])
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin", "Gumi"])
        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myQuestion.click_on_question_to_edit(1)
        #use a fail version of the function to save 200 seconds of timeout
        ex = mySurvey.myLogic.verify_funneling_disabled()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify disabled funneling",
                                 "Verifies that we cannnot add funneling to receiver question.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify disabled funneling"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_logic_funnelQuestion_selected(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test standard selected funneling.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin", "Gumi"])
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best German Kanmusu?", 1,
                                                          ["Graf Zeppelin", "Bismarck", "Prinz Eugen", "U-511"])
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myLogic.toggleQuestionFunneling()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks the preview button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.click_off_preview_warning()
        mySurvey.myDesign.switch_to_preview_iframe()
        # begin verification using rpage lib
        ex = mySurvey.myLogic.process_rPageMCQuestion("1", "1. Best Vocaloid?", "Miku")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question 1",
                                 "Verifies sender question.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify sender question."
        mySurvey.myDesign.previewNext()
        ex = mySurvey.myLogic.process_rPageMCQuestion("1", "2. Best German Kanmusu?", "Miku")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify selected answer receiver question",
                                 "Verifies that we can select funneled answer from sender.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify selected answer funneling."
        mySurvey.myDesign.click_preview_done_button()
        # mySurvey.myDesign.return_from_frame()
        myTitle = mySurvey.myDesign.getPreviewEndTitle()
        myBool = False
        if myTitle == "That's the end of the preview!":
            myBool = True
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check for ending survey page",
                                 "Check ending survey page.",
                                 myBool,
                                 True,
                                 not myBool,
                                 driver)
        assert myBool, "Failed to verify EOS page and funneling"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_logic_funnelQuestion_unselected(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test standard unselected funneling.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin", "Gumi"])
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best German Kanmusu?", 1,
                                                          ["Graf Zeppelin", "Bismarck", "Prinz Eugen", "U-511"])
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myLogic.toggleQuestionFunneling(selected=False)
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks the preview button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.click_off_preview_warning()
        mySurvey.myDesign.switch_to_preview_iframe()
        # begin verification using rpage lib
        ex = mySurvey.myLogic.process_rPageMCQuestion("1", "1. Best Vocaloid?", "Miku")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question 1",
                                 "Verifies sender question.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify sender question."
        mySurvey.myDesign.previewNext()
        ex = mySurvey.myLogic.process_rPageMCQuestion("1", "2. Best German Kanmusu?", "Luka")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify unselected answer receiver question",
                                 "Verifies that we can select unselected answer from sender.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify unselected answer funneling."
        mySurvey.myDesign.click_preview_done_button()
        # mySurvey.myDesign.return_from_frame()
        myTitle = mySurvey.myDesign.getPreviewEndTitle()
        myBool = False
        if myTitle == "That's the end of the preview!":
            myBool = True
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check for ending survey page",
                                 "Check ending survey page.",
                                 myBool,
                                 True,
                                 not myBool,
                                 driver)
        assert myBool, "Failed to verify EOS page and funneling"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_logic_funnelQuestion_dropdown(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test standard selected funneling with dropdown type.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_dropdown_question(
            mySurvey.survey_id, page_num,
            "Best Vocaloid?", 1, ["Miku", "Luka", "Rin"])
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best German Kanmusu?", 1,
                                                          ["Graf Zeppelin", "Bismarck", "Prinz Eugen", "U-511"])
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myLogic.toggleQuestionFunneling()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks the preview button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.click_off_preview_warning()
        mySurvey.myDesign.switch_to_preview_iframe()
        # begin verification using rpage lib
        ex = mySurvey.myLogic.process_rPageMCQuestion("1", "1. Best Vocaloid?", "Miku")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question 1",
                                 "Verifies sender question.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify sender question."
        mySurvey.myDesign.previewNext()
        ex = mySurvey.myLogic.process_rPageMCQuestion("1", "2. Best German Kanmusu?", "Miku")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify selected answer receiver question",
                                 "Verifies that we can select funneled answer from sender.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify selected answer funneling."
        mySurvey.myDesign.click_preview_done_button()
        # mySurvey.myDesign.return_from_frame()
        myTitle = mySurvey.myDesign.getPreviewEndTitle()
        myBool = False
        if myTitle == "That's the end of the preview!":
            myBool = True
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check for ending survey page",
                                 "Check ending survey page.",
                                 myBool,
                                 True,
                                 not myBool,
                                 driver)
        assert myBool, "Failed to verify EOS page and funneling"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_logic_funnelQuestion_matrix(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test standard selected funneling with matrix type.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_matrix_scale_question(mySurvey.survey_id, page_num,
                                                           "Please classify the following Ships", 1,
                                                           ["Haruna", "Yuudachi", "Naka"],
                                                           ["Destroyer(DD)", "Light Cruiser(CL)", "Battleship(BB)",
                                                            "Aircraft Carrier(CV)", "Submarine(SS)"])
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best German Kanmusu?", 1,
                                                          ["Graf Zeppelin", "Bismarck", "Prinz Eugen", "U-511"])
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myLogic.toggleQuestionFunneling()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks the preview button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.click_off_preview_warning()
        mySurvey.myDesign.switch_to_preview_iframe()
        # begin verification using rpage lib
        ex = mySurvey.myLogic.process_rPageMatrixQuestion("1", "1. Please classify the following Ships", "Yuudachi")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question 1",
                                 "Verifies sender question.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify sender question."
        mySurvey.myDesign.previewNext()
        ex = mySurvey.myLogic.process_rPageMCQuestion("1", "2. Best German Kanmusu?", "Yuudachi")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify selected answer receiver question",
                                 "Verifies that we can select funneled answer from sender.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify selected answer funneling."
        mySurvey.myDesign.click_preview_done_button()
        # mySurvey.myDesign.return_from_frame()
        myTitle = mySurvey.myDesign.getPreviewEndTitle()
        myBool = False
        if myTitle == "That's the end of the preview!":
            myBool = True
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check for ending survey page",
                                 "Check ending survey page.",
                                 myBool,
                                 True,
                                 not myBool,
                                 driver)
        assert myBool, "Failed to verify EOS page and funneling"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_logic_funnelQuestion_singleRowRating(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test unchecking single row rating scale checkbox after having carried forward responses.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best German Kanmusu?", 1,
                                                          ["Graf Zeppelin", "Bismarck", "Prinz Eugen", "U-511"])
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_matrix_scale_question(mySurvey.survey_id, page_num,
                                                           "Please classify the following Ships", 1,
                                                           ["Haruna", "Yuudachi", "Naka"],
                                                           ["Destroyer(DD)", "Light Cruiser(CL)", "Battleship(BB)",
                                                            "Aircraft Carrier(CV)", "Submarine(SS)"])
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myLogic.toggleQuestionFunneling()
        mySurvey.myQuestion.turn_on_setting("single_row_rating")
        ex = mySurvey.myQuestion.verify_removeFunnelDialog_modal()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify RemoveFunnel model",
                                 "Verifies that the RemoveFunnel model is open.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify RemoveFunnel model"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

def test_logic_funnelQuestion_icon(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test carried forward icon.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best German Kanmusu?", 1,
                                                          ["Graf Zeppelin", "Bismarck", "Prinz Eugen", "U-511"])
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_matrix_scale_question(mySurvey.survey_id, page_num,
                                                           "Please classify the following Ships", 1,
                                                           ["Haruna", "Yuudachi", "Naka"],
                                                           ["Destroyer(DD)", "Light Cruiser(CL)", "Battleship(BB)",
                                                            "Aircraft Carrier(CV)", "Submarine(SS)"])
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myLogic.toggleQuestionFunneling()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myDesign.scroll_to_top()
        ex = mySurvey.myQuestion.verify_funneling_icon()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify funneling icon",
                                 "Verifies that the funnelicon is displayed",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneling icon"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

def test_logic_funnelQuestion_otherOption(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "S page- Test funneling the text entered by the respondent into the next question from Other answer option as answer choice.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best German Kanmusu?", 1,
                                                          ["Graf Zeppelin", "Bismarck", "Prinz Eugen", "U-511"])
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.turn_on_multichoice_otheroption()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_matrix_scale_question(mySurvey.survey_id, page_num,
                                                           "Please classify the following Ships", 1,
                                                           ["Haruna", "Yuudachi", "Naka"],
                                                           ["Destroyer(DD)", "Light Cruiser(CL)", "Battleship(BB)",
                                                            "Aircraft Carrier(CV)", "Submarine(SS)"])
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myLogic.toggleQuestionFunneling()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks the preview button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.click_off_preview_warning()
        mySurvey.myDesign.switch_to_preview_iframe()
        # begin verification using rpage lib
        ex = mySurvey.myLogic.process_rPageMCQuestion("1", "1. Best German Kanmusu?", other="Tirpitz")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question 1",
                                 "Verifies sender question.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify sender question."
        mySurvey.myDesign.previewNext()
        ex = mySurvey.myLogic.process_rPageMatrixQuestion("1", "2. Please classify the following Ships", "Tirpitz")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify selected answer receiver question",
                                 "Verifies that we can select funneled other answer from sender.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify selected other answer funneling."
        mySurvey.myDesign.click_preview_done_button()
        #mySurvey.myDesign.return_from_frame()
        myTitle = mySurvey.myDesign.getPreviewEndTitle()
        myBool = False
        if myTitle == "That's the end of the preview!":
            myBool = True
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check for ending survey page",
                                 "Check ending survey page.",
                                 myBool,
                                 True,
                                 not myBool,
                                 driver)
        assert myBool, "Failed to verify EOS page and funneling"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

def test_logic_funnelQuestion_tooltip(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify funneling tooltips.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best German Kanmusu?", 1,
                                                          ["Graf Zeppelin", "Bismarck", "Prinz Eugen", "U-511"])
        mySurvey.myQuestion.click_on_question_to_edit(1)
        ex = mySurvey.myQuestion.verify_funneling_popup()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify funneling tooltip",
                                 "Verifies that funneling tooltip is working.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneling tooltip"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

def test_logic_funnelQuestion_answerChoiceSelected(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "S page- Test funneling answer choice (in receiver) question with selected answer choice (in sender).")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin", "Gumi"])
        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myLogic.toggleQuestionFunneling()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks the preview button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.click_off_preview_warning()
        mySurvey.myDesign.switch_to_preview_iframe()
        # begin verification using rpage lib
        ex = mySurvey.myLogic.process_rPageMCQuestion("1", "1. Best Vocaloid?", "Miku")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question 1",
                                 "Verifies sender question.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify sender question."
        mySurvey.myDesign.previewNext()
        ex = mySurvey.myLogic.process_rPageMCQuestion("1", "2. Best Kongou Class Ship?", "Miku")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify selected answer receiver question",
                                 "Verifies that we can select funneled answer from sender.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify selected answer funneling."
        mySurvey.myDesign.click_preview_done_button()
        # mySurvey.myDesign.return_from_frame()
        myTitle = mySurvey.myDesign.getPreviewEndTitle()
        myBool = False
        if myTitle == "That's the end of the preview!":
            myBool = True
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check for ending survey page",
                                 "Check ending survey page.",
                                 myBool,
                                 True,
                                 not myBool,
                                 driver)
        assert myBool, "Failed to verify EOS page and funneling"
        mySurvey.myDesign.return_from_preview_window()
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks the preview button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.click_off_preview_warning()
        mySurvey.myDesign.switch_to_preview_iframe()
        # begin verification using rpage lib
        mySurvey.myDesign.previewNext()
        # mySurvey.myDesign.return_from_frame()
        myTitle = mySurvey.myDesign.getPreviewEndTitle()
        myBool = False
        if myTitle == "That's the end of the preview!":
            myBool = True
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check for ending survey page",
                                 "Check ending survey page.",
                                 myBool,
                                 True,
                                 not myBool,
                                 driver)
        assert myBool, "Failed to verify receiver skipped when no sender selected"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_logic_funnelQuestion_answerChoiceUnselected(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "S page- Test funneling answer choice (in receiver) with unselected answer choice (in sender).")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin", "Gumi"])
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.turn_on_multiple_answers()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myLogic.toggleQuestionFunneling(selected=False)
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks the preview button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.click_off_preview_warning()
        mySurvey.myDesign.switch_to_preview_iframe()
        # begin verification using rpage lib
        ex = mySurvey.myLogic.process_rPageMCQuestion("1", "1. Best Vocaloid?", "Miku")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question 1",
                                 "Verifies sender question.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify sender question."
        mySurvey.myDesign.previewNext()
        ex = mySurvey.myLogic.process_rPageMCQuestion("1", "2. Best Kongou Class Ship?", "Luka")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify selected answer receiver question",
                                 "Verifies that we can select funneled answer from sender.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify selected answer funneling."
        mySurvey.myDesign.click_preview_done_button()
        # mySurvey.myDesign.return_from_frame()
        myTitle = mySurvey.myDesign.getPreviewEndTitle()
        myBool = False
        if myTitle == "That's the end of the preview!":
            myBool = True
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check for ending survey page",
                                 "Check ending survey page.",
                                 myBool,
                                 True,
                                 not myBool,
                                 driver)
        assert myBool, "Failed to verify EOS page and funneling"
        mySurvey.myDesign.return_from_preview_window()
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks the preview button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.click_off_preview_warning()
        mySurvey.myDesign.switch_to_preview_iframe()
        # begin verification using rpage lib
        ex = mySurvey.myLogic.process_rPageMCQuestion("1", "1. Best Vocaloid?", "Miku")
        ex = mySurvey.myLogic.process_rPageMCQuestion("1", "1. Best Vocaloid?", "Luka")
        ex = mySurvey.myLogic.process_rPageMCQuestion("1", "1. Best Vocaloid?", "Rin")
        ex = mySurvey.myLogic.process_rPageMCQuestion("1", "1. Best Vocaloid?", "Gumi")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question 1",
                                 "Verifies sender question.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify sender question."
        mySurvey.myDesign.previewNext()
        # mySurvey.myDesign.return_from_frame()
        myTitle = mySurvey.myDesign.getPreviewEndTitle()
        myBool = False
        if myTitle == "That's the end of the preview!":
            myBool = True
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check for ending survey page",
                                 "Check ending survey page.",
                                 myBool,
                                 True,
                                 not myBool,
                                 driver)
        assert myBool, "Failed to verify receiver skipped when no sender selected"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

def test_logic_funnelQuestion_deleteUserChoice(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test user entered (default choices) can be deleted and added.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin", "Gumi"])
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best German Kanmusu?", 1,
                                                          ["Graf Zeppelin", "Bismarck", "Prinz Eugen", "U-511"])
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myLogic.toggleQuestionFunneling()
        mySurvey.myQuestion.delete_multipleChoice_answerRow(4)
        mySurvey.myQuestion.delete_multipleChoice_answerRow(3)
        mySurvey.myQuestion.delete_multipleChoice_answerRow(2)
        mySurvey.myQuestion.delete_multipleChoice_answerRow(1)
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = True if mySurvey.myQuestion.verifyMultiChoiceQuestionAnswer(2, 1) == "Miku" and \
                        mySurvey.myQuestion.verifyMultiChoiceQuestionAnswer(2, 2) == "Luka" and \
                        mySurvey.myQuestion.verifyMultiChoiceQuestionAnswer(2, 3) == "Rin" and \
                        mySurvey.myQuestion.verifyMultiChoiceQuestionAnswer(2, 4) == "Gumi" else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify answer rows are only funneled rows",
                                 "Verifies that current answer rows are not user entered.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify deleted user entered answer rows."
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myLogic.toggleQuestionFunneling_fail()
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Prinz Eugen")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = True if mySurvey.myQuestion.verifyMultiChoiceQuestionAnswer(2, 1) == "Prinz Eugen" else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify answer rows are only user entered rows",
                                 "Verifies that user can re-enter answer rows after disabling funneling.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify user re-entered answer rows."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()