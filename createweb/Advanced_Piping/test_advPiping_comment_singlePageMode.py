from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


# Manually created survey for slider question
survey_dict = {

    'MT1': {'survey_id': '131190417', 'user_id': '61026099'},
    'MT2': {'survey_id': '131190417', 'user_id': '61026099'},
    'MT4': {'survey_id': '131190417', 'user_id': '61026099'}
    #todo: add other MT data
}




@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAdvPipingComment/",  # report_relative_location
                               "test_advPiping_comment_singlePageMode",  # report_file_name_prefix
                               "Verify advance piping from Comment qtype to all qtype except NPS",  # test_suite_title
                               ("This test adds comment type question "
                                " and then verifies advanced piping to all question type except NPS."),  # test_suite_description
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

def init_single_page_mode_survey(driver, mySurvey, report):
    survey_title = mySurvey.myCreate.get_survey_title()
    survey_info = survey_dict[pytest.config.option.domain.upper()[:3]]
    new_survey_id = mySurvey.myCreate.copy_exiting_survey_via_svysvc(survey_info["survey_id"],
                                                                      survey_info["user_id"],
                                                                      survey_title + "_Created_via_svysrv")
    url = mySurvey.myCreate.open_copied_survey(new_survey_id['survey_id'])
    driver.get(url)
    report.add_report_record(ReportMessageTypes.TEST_STEP,
                             "Survey Loaded or recreated",
                             "The survey has either been copied or recreated and is ready for the test",
                             True,
                             True,
                             False,
                             driver)
    mySurvey.myDesign.scroll_to_bottom()
    return new_survey_id['survey_id']

def test_advPiping_comment_singlePageMode_multiChoice(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify advance piping from Comment qtype to all qtype except NPS.")
    new_survey_id = init_single_page_mode_survey(driver, mySurvey, report)
    try:
        mySurvey.myBuilder.click_CommentBoxAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kanmusu?")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myCreate.single_page_goto(2)
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_multichoice_question(new_survey_id, page_num, "{{Q26}}", 1,
                                                          ["poi", "nanodesu", "Khorosho", "desu"])
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks preview button, in order to verify theme in preview window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        mySurvey.myDesign.click_off_preview_warning()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.switch_to_preview_iframe()
        mySurvey.myLogic.enter_textType_preview_answer(26, "Yuudachi")
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title("Yuudachi")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q26",
                                 "Verify question title is the same that we entered in Q26.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question title piping"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advPiping_comment_singlePageMode_dropdown(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify advance piping from Comment qtype to dropdown type question.")
    new_survey_id = init_single_page_mode_survey(driver, mySurvey, report)
    try:
        mySurvey.myBuilder.click_CommentBoxAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kanmusu?")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myCreate.single_page_goto(2)
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_dropdown_question(
            new_survey_id, page_num,
            "{{Q26}}", 1, ["Miku", "Luka", "Rin"])
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks preview button, in order to verify theme in preview window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        mySurvey.myDesign.click_off_preview_warning()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.switch_to_preview_iframe()
        mySurvey.myLogic.enter_textType_preview_answer(26, "Yuudachi")
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title("Yuudachi")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q26",
                                 "Verify question title is the same that we entered in Q26.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question title piping"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advPiping_comment_singlePageMode_matrix(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify advance piping from Comment qtype to matrix type question.")
    new_survey_id = init_single_page_mode_survey(driver, mySurvey, report)
    try:
        mySurvey.myBuilder.click_CommentBoxAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kanmusu?")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myCreate.single_page_goto(2)
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_matrix_scale_question(new_survey_id, page_num,
                                                           "{{Q26}}", 1,
                                                           ["Haruna", "Yuudachi", "Naka"],
                                                           ["Destroyer(DD)", "Light Cruiser(CL)", "Battleship(BB)",
                                                            "Aircraft Carrier(CV)", "Submarine(SS)"])
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks preview button, in order to verify theme in preview window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        mySurvey.myDesign.click_off_preview_warning()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.switch_to_preview_iframe()
        mySurvey.myLogic.enter_textType_preview_answer(26, "Yuudachi")
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title("Yuudachi")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q26",
                                 "Verify question title is the same that we entered in Q26.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question title piping"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advPiping_comment_singlePageMode_menuMatrix(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify advance piping from Comment qtype to menu matrix type question.")
    new_survey_id = init_single_page_mode_survey(driver, mySurvey, report)
    try:
        mySurvey.myBuilder.click_CommentBoxAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kanmusu?")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myCreate.single_page_goto(2)
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_menu_matrix_question(
            new_survey_id, page_num,
            "{{Q26}}", 1)
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks preview button, in order to verify theme in preview window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        mySurvey.myDesign.click_off_preview_warning()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.switch_to_preview_iframe()
        mySurvey.myLogic.enter_textType_preview_answer(26, "Yuudachi")
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title("Yuudachi")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q26",
                                 "Verify question title is the same that we entered in Q26.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question title piping"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advPiping_comment_singlePageMode_ranking(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify advance piping from Comment qtype to ranking type question.")
    new_survey_id = init_single_page_mode_survey(driver, mySurvey, report)
    try:
        mySurvey.myBuilder.click_CommentBoxAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kanmusu?")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myCreate.single_page_goto(2)
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_ranking_question(new_survey_id, page_num, "{{Q26}}", 1)
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks preview button, in order to verify theme in preview window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        mySurvey.myDesign.click_off_preview_warning()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.switch_to_preview_iframe()
        mySurvey.myLogic.enter_textType_preview_answer(26, "Yuudachi")
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title("Yuudachi")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q26",
                                 "Verify question title is the same that we entered in Q26.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question title piping"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advPiping_comment_singlePageMode_singleTextbox(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify advance piping from Comment qtype to Single Textbox type question.")
    new_survey_id = init_single_page_mode_survey(driver, mySurvey, report)
    try:
        mySurvey.myBuilder.click_CommentBoxAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kanmusu?")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        
        mySurvey.myCreate.single_page_goto(2)
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_single_textbox_question(
            new_survey_id, page_num,
            "{{Q26}}", 1)
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks preview button, in order to verify theme in preview window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        mySurvey.myDesign.click_off_preview_warning()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.switch_to_preview_iframe()
        mySurvey.myLogic.enter_textType_preview_answer(26, "Yuudachi")
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title("Yuudachi")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q26",
                                 "Verify question title is the same that we entered in Q26.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question title piping"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advPiping_comment_singlePageMode_multiTextbox(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify advance piping from Comment qtype to Multi Textbox type question.")
    new_survey_id = init_single_page_mode_survey(driver, mySurvey, report)
    try:
        mySurvey.myBuilder.click_CommentBoxAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kanmusu?")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        
        mySurvey.myCreate.single_page_goto(2)
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_multi_textbox_question(
            new_survey_id, page_num,
            "{{Q26}}", 1)
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks preview button, in order to verify theme in preview window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        mySurvey.myDesign.click_off_preview_warning()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.switch_to_preview_iframe()
        mySurvey.myLogic.enter_textType_preview_answer(26, "Yuudachi")
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title("Yuudachi")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q26",
                                 "Verify question title is the same that we entered in Q26.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question title piping"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advPiping_comment_singlePageMode_commentBox(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify advance piping from Comment qtype to Comment Box type question.")
    new_survey_id = init_single_page_mode_survey(driver, mySurvey, report)
    try:
        mySurvey.myBuilder.click_CommentBoxAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kanmusu?")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        
        mySurvey.myCreate.single_page_goto(2)
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_comment_box_question(
            new_survey_id, page_num,
            "{{Q26}}", 1)
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks preview button, in order to verify theme in preview window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        mySurvey.myDesign.click_off_preview_warning()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.switch_to_preview_iframe()
        mySurvey.myLogic.enter_textType_preview_answer(26, "Yuudachi")
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title("Yuudachi")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q26",
                                 "Verify question title is the same that we entered in Q26.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question title piping"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advPiping_comment_singlePageMode_contactInfo(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify advance piping from Comment qtype to Contact Info type question.")
    new_survey_id = init_single_page_mode_survey(driver, mySurvey, report)
    try:
        mySurvey.myBuilder.click_CommentBoxAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kanmusu?")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        
        mySurvey.myCreate.single_page_goto(2)
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_address_question(
            new_survey_id, page_num,
            "{{Q26}}", 1)
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks preview button, in order to verify theme in preview window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        mySurvey.myDesign.click_off_preview_warning()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.switch_to_preview_iframe()
        mySurvey.myLogic.enter_textType_preview_answer(26, "Yuudachi")
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title("Yuudachi")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q26",
                                 "Verify question title is the same that we entered in Q26.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question title piping"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advPiping_comment_singlePageMode_dateTime(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify advance piping from Comment qtype to DateTime type question.")
    new_survey_id = init_single_page_mode_survey(driver, mySurvey, report)
    try:
        mySurvey.myBuilder.click_CommentBoxAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kanmusu?")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myCreate.single_page_goto(2)
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_date_time_question(
            new_survey_id, page_num,
            "{{Q26}}", 1)
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks preview button, in order to verify theme in preview window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        mySurvey.myDesign.click_off_preview_warning()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.switch_to_preview_iframe()
        mySurvey.myLogic.enter_textType_preview_answer(26, "Yuudachi")
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title("Yuudachi")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q26",
                                 "Verify question title is the same that we entered in Q26.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question title piping"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advPiping_comment_singlePageMode_text(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify advance piping from Comment qtype to Text type question.")
    new_survey_id = init_single_page_mode_survey(driver, mySurvey, report)
    try:
        mySurvey.myBuilder.click_CommentBoxAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kanmusu?")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myCreate.single_page_goto(2)
        mySurvey.myBuilder.click_TextAddButton()
        mySurvey.myQuestion.enter_text_question_title("{{Q26}}")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks preview button, in order to verify theme in preview window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        mySurvey.myDesign.click_off_preview_warning()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.switch_to_preview_iframe()
        mySurvey.myLogic.enter_textType_preview_answer(26, "Yuudachi")
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.get_preview_text(26, "Yuudachi")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q26",
                                 "Verify question title is the same that we entered in Q26.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question title piping"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advPiping_comment_singlePageMode_image(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify advance piping from Comment qtype to Image type question.")
    new_survey_id = init_single_page_mode_survey(driver, mySurvey, report)
    try:
        mySurvey.myBuilder.click_CommentBoxAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kanmusu?")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myCreate.single_page_goto(2)
        mySurvey.myBuilder.click_ImageAddButton()
        mySurvey.myQuestion.enter_image_label("{{Q26}}", 1)
        mySurvey.myQuestion.click_imageURL_radioButton()
        mySurvey.myQuestion.enter_image_url("https://secure.surveymonkey.com/smassets/smlib.globaltemplates/1.4.7/assets/logo/surveymonkey_logo.svg")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks preview button, in order to verify theme in preview window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        mySurvey.myDesign.click_off_preview_warning()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.switch_to_preview_iframe()
        mySurvey.myLogic.enter_textType_preview_answer(26, "Yuudachi")
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.get_preview_image_label(26, "Yuudachi")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q26",
                                 "Verify question title is the same that we entered in Q26.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question title piping"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advPiping_comment_singlePageMode_textAB(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify advance piping from Comment qtype to TextAB  type question.")
    new_survey_id = init_single_page_mode_survey(driver, mySurvey, report)
    try:
        mySurvey.myBuilder.click_CommentBoxAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kanmusu?")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myCreate.single_page_goto(2)
        mySurvey.myBuilder.click_TextABTestAddButton()
        mySurvey.myQuestion.enter_textAB_textbox(1, "{{Q26}}")
        mySurvey.myQuestion.enter_textAB_textbox(2, "{{Q26}}")  # for some reason it eats one of the opening curly braces O_O
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks preview button, in order to verify theme in preview window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        mySurvey.myDesign.click_off_preview_warning()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.switch_to_preview_iframe()
        mySurvey.myLogic.enter_textType_preview_answer(26, "Yuudachi")
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.get_preview_text(26, "Yuudachi")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q26",
                                 "Verify question title is the same that we entered in Q26.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question title piping"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advPiping_comment_singlePageMode_imageAB(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify advance piping from Comment qtype to ImageAB type question.")
    new_survey_id = init_single_page_mode_survey(driver, mySurvey, report)
    try:
        mySurvey.myBuilder.click_CommentBoxAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kanmusu?")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myCreate.single_page_goto(2)
        mySurvey.myBuilder.click_ImageABTestAddButton()
        mySurvey.myQuestion.enter_imageAB_label(1, "{{Q26}}")
        mySurvey.myQuestion.enter_imageAB_url(1,
                                              "http://images5.fanpop.com/image/photos/31100000/"
                                              "Keep-Calm-and-Continue-Testing-portal-2-31140076-453-700.jpg")
        mySurvey.myQuestion.enter_imageAB_label(2, "{{Q26}}")  # First curly brace gets eaten by webdriver
        mySurvey.myQuestion.enter_imageAB_url(2,
                                              "http://images4.fanpop.com/image/photos/21200000"
                                              "/TACOS-gir-21208550-838-953.jpg")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks preview button, in order to verify theme in preview window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        mySurvey.myDesign.click_off_preview_warning()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.switch_to_preview_iframe()
        mySurvey.myLogic.enter_textType_preview_answer(26, "Yuudachi")
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.get_preview_image_label(26, "Yuudachi")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q26",
                                 "Verify question title is the same that we entered in Q26.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question title piping"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()