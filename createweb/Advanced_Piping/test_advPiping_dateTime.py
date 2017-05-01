from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest
from datetime import datetime


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAdvPipingComment/",  # report_relative_location
                               "test_advPiping_dateTime",  # report_file_name_prefix
                               "verify advance piping from dateTime qtype to all qtype except NPS",  # test_suite_title
                               ("This test adds date time type question "
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


def test_advPiping_dateTime_multiChoice(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify advance piping from dateTime qtype to all qtype except NPS.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_date_time_question(
            mySurvey.survey_id, page_num,
            "Best Vocaloid?", 1)
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "{{Q1}}", 1,
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
        myTime = datetime.now()
        mySurvey.myDesign.enter_dateTime_preview(1, myTime)
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title(myTime.strftime("%m/%d/%Y %I:%M %p"))
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q1",
                                 "Verify question title is the same that we entered in Q1.",
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


def test_advPiping_dateTime_dropdown(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify advance piping from dateTime qtype to dropdown type question.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_date_time_question(
            mySurvey.survey_id, page_num,
            "Best Vocaloid?", 1)
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_dropdown_question(
            mySurvey.survey_id, page_num,
            "{{Q1}}", 1, ["Miku", "Luka", "Rin"])
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
        myTime = datetime.now()
        mySurvey.myDesign.enter_dateTime_preview(1, myTime)
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title(myTime.strftime("%m/%d/%Y %I:%M %p"))
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q1",
                                 "Verify question title is the same that we entered in Q1.",
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


def test_advPiping_dateTime_matrix(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify advance piping from dateTime qtype to matrix type question.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_date_time_question(
            mySurvey.survey_id, page_num,
            "Best Vocaloid?", 1)
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_matrix_scale_question(mySurvey.survey_id, page_num,
                                                           "{{Q1}}", 1,
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
        myTime = datetime.now()
        mySurvey.myDesign.enter_dateTime_preview(1, myTime)
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title(myTime.strftime("%m/%d/%Y %I:%M %p"))
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q1",
                                 "Verify question title is the same that we entered in Q1.",
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


def test_advPiping_dateTime_menuMatrix(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify advance piping from dateTime qtype to menu matrix type question.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_date_time_question(
            mySurvey.survey_id, page_num,
            "Best Vocaloid?", 1)
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_menu_matrix_question(
            mySurvey.survey_id, page_num,
            "{{Q1}}", 1)
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
        myTime = datetime.now()
        mySurvey.myDesign.enter_dateTime_preview(1, myTime)
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title(myTime.strftime("%m/%d/%Y %I:%M %p"))
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q1",
                                 "Verify question title is the same that we entered in Q1.",
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


def test_advPiping_dateTime_ranking(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify advance piping from dateTime qtype to ranking type question.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_date_time_question(
            mySurvey.survey_id, page_num,
            "Best Vocaloid?", 1)
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_ranking_question(mySurvey.survey_id, page_num, "{{Q1}}", 1)
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
        myTime = datetime.now()
        mySurvey.myDesign.enter_dateTime_preview(1, myTime)
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title(myTime.strftime("%m/%d/%Y %I:%M %p"))
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q1",
                                 "Verify question title is the same that we entered in Q1.",
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


def test_advPiping_dateTime_singleTextbox(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify advance piping from dateTime qtype to Single Textbox type question.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_date_time_question(
            mySurvey.survey_id, page_num,
            "Best Vocaloid?", 1)
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_single_textbox_question(
            mySurvey.survey_id, page_num,
            "{{Q1}}", 1)
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
        myTime = datetime.now()
        mySurvey.myDesign.enter_dateTime_preview(1, myTime)
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title(myTime.strftime("%m/%d/%Y %I:%M %p"))
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q1",
                                 "Verify question title is the same that we entered in Q1.",
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


def test_advPiping_dateTime_multiTextbox(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify advance piping from dateTime qtype to Multi Textbox type question.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_date_time_question(
            mySurvey.survey_id, page_num,
            "Best Vocaloid?", 1)
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_multi_textbox_question(
            mySurvey.survey_id, page_num,
            "{{Q1}}", 1)
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
        myTime = datetime.now()
        mySurvey.myDesign.enter_dateTime_preview(1, myTime)
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title(myTime.strftime("%m/%d/%Y %I:%M %p"))
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q1",
                                 "Verify question title is the same that we entered in Q1.",
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


def test_advPiping_dateTime_commentBox(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify advance piping from dateTime qtype to Comment Box type question.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_date_time_question(
            mySurvey.survey_id, page_num,
            "Best Vocaloid?", 1)
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_comment_box_question(
            mySurvey.survey_id, page_num,
            "{{Q1}}", 1)
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
        myTime = datetime.now()
        mySurvey.myDesign.enter_dateTime_preview(1, myTime)
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title(myTime.strftime("%m/%d/%Y %I:%M %p"))
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q1",
                                 "Verify question title is the same that we entered in Q1.",
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


def test_advPiping_dateTime_contactInfo(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify advance piping from dateTime qtype to Contact Info type question.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_date_time_question(
            mySurvey.survey_id, page_num,
            "Best Vocaloid?", 1)
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_address_question(
            mySurvey.survey_id, page_num,
            "{{Q1}}", 1)
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
        myTime = datetime.now()
        mySurvey.myDesign.enter_dateTime_preview(1, myTime)
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title(myTime.strftime("%m/%d/%Y %I:%M %p"))
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q1",
                                 "Verify question title is the same that we entered in Q1.",
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


def test_advPiping_dateTime_dateTime(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify advance piping from dateTime qtype to DateTime type question.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_date_time_question(
            mySurvey.survey_id, page_num,
            "Best Vocaloid?", 1)
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_date_time_question(
            mySurvey.survey_id, page_num,
            "{{Q1}}", 1)
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
        myTime = datetime.now()
        mySurvey.myDesign.enter_dateTime_preview(1, myTime)
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title(myTime.strftime("%m/%d/%Y %I:%M %p"))
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q1",
                                 "Verify question title is the same that we entered in Q1.",
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


def test_advPiping_dateTime_text(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify advance piping from dateTime qtype to Text type question.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_date_time_question(
            mySurvey.survey_id, page_num,
            "Best Vocaloid?", 1)
        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myBuilder.click_TextAddButton()
        mySurvey.myQuestion.enter_text_question_title("{{Q1}}")
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
        myTime = datetime.now()
        mySurvey.myDesign.enter_dateTime_preview(1, myTime)
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.get_preview_text(1, myTime.strftime("%m/%d/%Y %I:%M %p"))
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q1",
                                 "Verify question title is the same that we entered in Q1.",
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


def test_advPiping_dateTime_image(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify advance piping from dateTime qtype to Image type question.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_date_time_question(
            mySurvey.survey_id, page_num,
            "Best Vocaloid?", 1)
        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myBuilder.click_ImageAddButton()
        mySurvey.myQuestion.enter_image_label("{{Q1}}", 1)
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
        myTime = datetime.now()
        mySurvey.myDesign.enter_dateTime_preview(1, myTime)
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.get_preview_image_label(1, myTime.strftime("%m/%d/%Y %I:%M %p"))
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q1",
                                 "Verify question title is the same that we entered in Q1.",
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


def test_advPiping_dateTime_textAB(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify advance piping from dateTime qtype to TextAB  type question.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_date_time_question(
            mySurvey.survey_id, page_num,
            "Best Vocaloid?", 1)
        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myBuilder.click_TextABTestAddButton()
        mySurvey.myQuestion.enter_textAB_textbox(1, "{{Q1}}")
        mySurvey.myQuestion.enter_textAB_textbox(2, "{{Q1}}")  # webdriver eats one of the opening curly braces
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
        myTime = datetime.now()
        mySurvey.myDesign.enter_dateTime_preview(1, myTime)
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.get_preview_text(1, myTime.strftime("%m/%d/%Y %I:%M %p"))
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q1",
                                 "Verify question title is the same that we entered in Q1.",
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


def test_advPiping_dateTime_imageAB(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify advance piping from dateTime qtype to ImageAB type question.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_date_time_question(
            mySurvey.survey_id, page_num,
            "Best Vocaloid?", 1)
        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myBuilder.click_ImageABTestAddButton()
        mySurvey.myQuestion.enter_imageAB_label(1, "{{Q1}}")
        mySurvey.myQuestion.enter_imageAB_url(1,
                                              "http://images5.fanpop.com/image/photos/31100000/"
                                              "Keep-Calm-and-Continue-Testing-portal-2-31140076-453-700.jpg")
        mySurvey.myQuestion.enter_imageAB_label(2, "{{Q1}}")  # First curly brace gets eaten by webdriver
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
        myTime = datetime.now()
        mySurvey.myDesign.enter_dateTime_preview(1, myTime)
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.get_preview_image_label(1, myTime.strftime("%m/%d/%Y %I:%M %p"))
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q1",
                                 "Verify question title is the same that we entered in Q1.",
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