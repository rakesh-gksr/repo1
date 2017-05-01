from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):

    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifyTextDirectionForExistingQuestionFields/",  # report_relative_location
                               "test_verifyTextDirectionForExistingQuestionFields",  # report_file_name_prefix
                               "Verify that for an existing field with text we don't change the direction to "
                               "rtl even though language is rtl. In this case user would need to use the buttons "
                               "for changing the direction.",  # test_suite_title
                               ("Test to Verify that for an existing field with text we don't change the direction "
                                "to rtl even though language is rtl. In this case user would need to use the "
                                "buttons for changing the direction."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d,"
                                                                                                      " %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.RTL
@pytest.mark.C7133050
def test_verify_text_direction_for_existing_question_fields(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify that for an existing field with text we "
                                                           "don't change the direction to rtl even though language "
                                                           "is rtl. In this case user would need to use the buttons "
                                                           "for changing the direction.")
    try:
        mySurvey.myDesign.modifySurveyTitle("test_RTL Support")
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Multiple Choice question saved",
                                 "Verified that Multiple Choice question is saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Multiple Choice question is saved."
        mySurvey.myOptions.unfold_OptionsRegion()
        mySurvey.myOptions.languageSelect("Arabic", mySurvey)
        mySurvey.myQuestion.click_on_question_to_edit(1)
        ex = mySurvey.myQuestion.verify_ltr_text_direction_in_question_field()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify text direction(LTR) in question title field",
                                 "verifies that Question title is set in LTR only despite the RTL language",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Question title is set in LTR only despite the RTL language"

        # Code to verify whether the answer choices saved with text in right to left direction

        ex = mySurvey.myQuestion.verify_ltr_text_direction_in_answer_field(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify text direction(LTR) in answer field",
                                 "verifies that answer choices are is set in LTR only despite the RTL language",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that answer choices are is set in LTR only despite the RTL language"
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        ex = mySurvey.myQuestion.verify_rtl_text_direction_in_question_field("Please classify the following Ships")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify text direction in question title field",
                                 "verifies that text direction in question title field is Right ",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that text direction in question title field is Right"
        ex = mySurvey.myQuestion.verify_rtl_text_direction_in_answer_field(1, "Haruna")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify text direction in answer field",
                                 "verifies that text direction in answer field field is Right",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that text direction in answer field is Right"
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Second Multiple Choice question saved",
                                 "Verified that second Multiple Choice question is saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that second Multiple Choice question is saved."

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
