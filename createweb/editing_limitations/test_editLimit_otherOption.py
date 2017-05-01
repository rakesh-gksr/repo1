from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestEditLimitOtherOption/",  # report_relative_location
                               "test_editLimit_otherOption",  # report_file_name_prefix
                               "Dropdown:verify add other answer options",  # test_suite_title
                               ("This test adds 2 dropdowns, 1 with other answer enabled. Answers are collected "
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


def test_editLimit_otherOption(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Dropdown:verify add other answer options.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_DropdownAddButton()
        mySurvey.myQuestion.enter_question_title("Best Vocaloid?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Miku")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Luka")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Rin")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_DropdownAddButton()
        mySurvey.myQuestion.enter_question_title("This wormhole leads to...")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "A room with a moose")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Fluffy Pillows")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Pixels")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myQuestion.click_on_question_to_edit()
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
        # begin verification using rpage lib
        mySurvey.myLogic.process_surveyCollection(mySurvey.myCreate.get_survey_title(), [{1: {'choices_list': ['Miku']}}])
        mySurvey.myQuestion.click_on_question_to_edit()
        ex = mySurvey.myQuestion.verify_responsesCollected()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify questions collected succesfully",
                                 "checks for limited editability notice",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify limited editability."
        mySurvey.myQuestion.turn_off_multichoice_otheroption()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_otherAnswer_textBox(1)
        ex = not ex
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Other Answer Disabled",
                                 "Checks for other answer text box removal",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify other answer disabled."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
