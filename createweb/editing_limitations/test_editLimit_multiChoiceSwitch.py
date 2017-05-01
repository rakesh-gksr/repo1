from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestEditLimitMultiChoiceSwitch/",  # report_relative_location
                               "test_editLimit_multiChoiceSwitch",  # report_file_name_prefix
                               # test_suite_title
                               "multiple choice: verify you can't switch from single answer to multiple answer and vice versa, also add other answer options limitation ",
                               ("Adds 2 MC questions and enabled multi answer. Survey answers are collected"
                                " and verifies that limited editability is enabled."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_editLimit_multiChoiceSwitch(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "multiple choice: verify you can't switch from single answer to multiple answer and vice versa, also add other answer options limitation.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("Best Vocaloid?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Miku")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Luka")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Rin")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myQuestion.click_on_question_to_edit(1)
        ex = mySurvey.myQuestion.turn_on_multiple_answers()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify multiple answers enabled",
                                 "checks for multiple answers",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify multiple answers enabled."
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myLogic.process_surveyCollection(mySurvey.myCreate.get_survey_title(), [{1: {'choices_list': ['Kongou']}}])
        mySurvey.myQuestion.click_on_question_to_edit(1)
        ex = mySurvey.myQuestion.verify_responsesCollected()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify questions collected succesfully",
                                 "checks for limited editability notice",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify limited editability."
        ex = mySurvey.myQuestion.turn_off_multiple_answers()
        ex = not ex
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify multiple answers checkbox disabled",
                                 "checks to make sure user can not disable multiple answers after answers collected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify limited multiple answers checkbox disabled."
        mySurvey.myQuestion.turn_on_multichoice_otheroption()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_otherAnswer_textBox(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Other Answer Enabled",
                                 "Checks for other answer text box",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify other answer enabled."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test ",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
