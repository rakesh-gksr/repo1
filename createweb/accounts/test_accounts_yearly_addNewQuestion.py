from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAccountsYearlyAddNewQuestion/",  # report_relative_location
                               "test_accounts_yearly_addNewQuestion",  # report_file_name_prefix
                               " Verify Add New Question button",  # test_suite_title
                               ("This test tests adding questions via the add new question button "
                                " and verifies question is added."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init('YEARLY')
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_accounts_yearly_addNewQuestion_default(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button.")
    try:
        mySurvey.myCreate.add_a_new_question()
        ex = True if mySurvey.myQuestion.get_question_type_of_current_editing() == "single_choice_vertical" else False
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is multiple choice",
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

def test_accounts_yearly_addNewQuestion_multipleChoice(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (MultiChoice).")
    try:
        mySurvey.myCreate.add_a_new_question("MultipleChoice")
        ex = True if mySurvey.myQuestion.get_question_type_of_current_editing() == "single_choice_vertical" else False
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is multiple choice",
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

def test_accounts_yearly_addNewQuestion_dropdown(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (Dropdown).")
    try:
        mySurvey.myCreate.add_a_new_question("Dropdown")
        ex = True if mySurvey.myQuestion.get_question_type_of_current_editing() == "single_choice_menu" else False
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is dropdown",
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

def test_accounts_yearly_addNewQuestion_matrix(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (Matrix).")
    try:
        mySurvey.myCreate.add_a_new_question("Matrix")
        ex = True if mySurvey.myQuestion.get_question_type_of_current_editing() == "matrix_rating" else False
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is matrix",
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

def test_accounts_yearly_addNewQuestion_menuMatrix(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (Menu Matrix).")
    try:
        mySurvey.myCreate.add_a_new_question("MenuMatrix")
        ex = True if mySurvey.myQuestion.get_question_type_of_current_editing() == "matrix_menu" else False
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is menu matrix",
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

def test_accounts_yearly_addNewQuestion_ranking(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (Ranking).")
    try:
        mySurvey.myCreate.add_a_new_question("Ranking")
        ex = True if mySurvey.myQuestion.get_question_type_of_current_editing() == "matrix_ranking" else False
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is matrix",
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

def test_accounts_yearly_addNewQuestion_NPS(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (NPS).")
    try:
        mySurvey.myCreate.add_a_new_question("QB-net_promoter_score")
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
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

def test_accounts_yearly_addNewQuestion_singleTextbox(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (Single Textbox).")
    try:
        mySurvey.myCreate.add_a_new_question("SingleTextbox")
        ex = True if mySurvey.myQuestion.get_question_type_of_current_editing() == "open_ended_single" else False
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is Single Textbox",
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

def test_accounts_yearly_addNewQuestion_multiTextbox(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (Multi Textbox).")
    try:
        mySurvey.myCreate.add_a_new_question("MultipleTextbox")
        ex = True if mySurvey.myQuestion.get_question_type_of_current_editing() == "open_ended_multi" else False
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is Multiple Textboxes",
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

def test_accounts_yearly_addNewQuestion_commentBox(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (Comment Box).")
    try:
        mySurvey.myCreate.add_a_new_question("CommentBox")
        ex = True if mySurvey.myQuestion.get_question_type_of_current_editing() == "open_ended_essay" else False
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is Comment Box",
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

def test_accounts_yearly_addNewQuestion_contactInfo(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (Contact Info).")
    try:
        mySurvey.myCreate.add_a_new_question("ContactInfo")
        ex = True if mySurvey.myQuestion.get_question_type_of_current_editing() == "demographic_international" else False
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is Contact Info",
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

def test_accounts_yearly_addNewQuestion_dateTime(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (DateTime).")
    try:
        mySurvey.myCreate.add_a_new_question("DateTime")
        ex = True if mySurvey.myQuestion.get_question_type_of_current_editing() == "datetime_both" else False
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify newly added question",
                                 "Checks newly added question is Date Time",
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

def test_accounts_yearly_addNewQuestion_text(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (Text).")
    try:
        mySurvey.myCreate.add_a_new_question("Text")
        ex = True if mySurvey.myQuestion.get_question_type_of_current_editing() == "presentation_descriptive_text" else False
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

def test_accounts_yearly_addNewQuestion_Image(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (Image).")
    try:
        mySurvey.myCreate.add_a_new_question("Image")
        ex = True if mySurvey.myQuestion.get_question_type_of_current_editing() == "presentation_image" else False
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

def test_accounts_yearly_addNewQuestion_textAB(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (TextAB).")
    try:
        mySurvey.myCreate.add_a_new_question("upgradeRandomAssignment", "rct")
        ex = mySurvey.myLogic.verify_upgradeNotify("RandomAssignment")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify upgrade notification for text A/B Test feature",
                                 "verifies select user gets upgrade notification for text A/B Test type question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify upgrade notification for text A/B Test."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

def test_accounts_yearly_addNewQuestion_imageAB(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " Verify add a new question button via dropdown (ImageAB).")
    try:
        mySurvey.myCreate.add_a_new_question("upgradeRandomAssignment", "rci")
        ex = mySurvey.myLogic.verify_upgradeNotify("RandomAssignment")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify upgrade notification for image A/B Test feature",
                                 "verifies select user gets upgrade notification for image A/B Test type question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify upgrade notification for image A/B Test."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
