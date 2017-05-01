from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestEditLimitQuota/",  # report_relative_location
                               "test_editLimit_quota",  # report_file_name_prefix
                               "Verify editing limitations on quota qualified questions",  # test_suite_title
                               ("Adds affected question types and options, collects answers"
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


def test_editLimit_quota(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify editing limitations on quota qualified questions.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_DropdownAddButton()
        mySurvey.myQuestion.enter_question_title("Best Vocaloid?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Miku")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Luka")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Rin")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_Quota()
        mySurvey.myLogic.quotaSetupWizard("simple", 1, 1, [1, 2])
        ex = mySurvey.myLogic.checkQuotaIcon(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page quota icon appears",
                                 "checks to make sure that the page quota icon appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page quota icon"
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.turn_on_multichoice_otheroption()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myLogic.process_surveyCollection(
            mySurvey.myCreate.get_survey_title(), [{1: {'choices_list': ['Kirishima']}, 2:{'choices_list': ['Miku']}}])
        mySurvey.myQuestion.click_on_question_to_edit()
        ex = mySurvey.myQuestion.verify_responsesCollected()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify questions collected succesfully",
                                 "checks for limited editability notice multiple choice",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify limited editability multiple choice."
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
        mySurvey.myQuestion.click_on_question_to_edit(2)
        ex = mySurvey.myQuestion.verify_responsesCollected()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify questions collected succesfully",
                                 "checks for limited editability notice dropdown",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify limited editability dropdown."
        ex = mySurvey.myLogic.toggleQuestionFunneling()
        ex = not ex
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify funneling disabled",
                                 "checks for disabled funneling toggle",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneling toggle."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test ",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
