from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from dynamic_tests.dynamic_tests_config import test_data_for_verifying_saved_rtl_direction
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):

    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifySaveTextDirection/",  # report_relative_location
                               "test_verifySaveTextDirection",  # report_file_name_prefix
                               "Verify you can change the direction and save using both rtl as well as ltr buttons.",
                               # test_suite_title
                               ("Test to verify you can change the direction and save using both rtl as well "
                                "as ltr buttons."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, "
                                                                                                      "%Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.IB
@pytest.mark.RIL
@pytest.mark.C7133049
@pytest.mark.C21160227
@pytest.mark.C21160228
@pytest.mark.parametrize("test_data", test_data_for_verifying_saved_rtl_direction,
                         ids=[dict['test_rail_id'] for dict in test_data_for_verifying_saved_rtl_direction])
def test_verify_save_text_direction(create_survey, test_data):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, test_data["test_case_title"])
    try:
        mySurvey.myDesign.modifySurveyTitle("test_RTL Support")
        mySurvey.myOptions.unfold_OptionsRegion()
        mySurvey.myOptions.languageSelect(test_data["language"], mySurvey)
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        ex = mySurvey.myQuestion.verify_rtl_text_direction_in_question_field("Please classify the following Ships")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify text direction in question title field for " +
                                 test_data["language"] + " language",
                                 "verifies that text direction in question title field is Right for " +
                                 test_data["language"] + " language",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that text direction in question title field is Right for  " \
                   + test_data["language"] + " language"
        ex = mySurvey.myQuestion.verify_rtl_text_direction_in_answer_field(1, "Haruna")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify text direction in answer field for " +
                                 test_data["language"] + " language",
                                 "verifies that text direction in answer field field is Right for " +
                                 test_data["language"] + " language",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that text direction in answer field is Right for  " \
                   + test_data["language"] + " language"

        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)

        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question saved with RTL language",
                                 "Verified that question saved with RTL language for question title and answer choices",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that question saved with RTL language for question title and answer choice."

        # Code to verify whether the question title saved with text in right to left direction

        mySurvey.myQuestion.click_on_question_to_edit()
        ex = mySurvey.myQuestion.verify_rtl_text_direction_in_question_field(False)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify text direction(RTL) in question title "
                                                               "field for " + test_data["language"] + " language",
                                 "verifies that text direction in question title field is Right for " +
                                 test_data["language"] + " language",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that text direction in question title field is Right for  " \
                   + test_data["language"] + " language"

        # Code to verify whether the answer choices saved with text in right to left direction

        ex = mySurvey.myQuestion.verify_rtl_text_direction_in_answer_field(1, False)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify text direction(RTL) in answer field for " +
                                 test_data["language"] + " language",
                                 "verifies that text direction in answer field field is Right for " +
                                 test_data["language"] + " language",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that text direction in answer field is Right for  " \
                   + test_data["language"] + " language"

        # Now change the question text direction to left to right

        ex = mySurvey.myQuestion.change_question_text_direction_to_ltr()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Change text direction in question title field for " +
                                 test_data["language"] + " language",
                                 "Change and verifies that text direction in question title field is Left for " +
                                 test_data["language"] + " language",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to change and verify that text direction in question title field is Left for  " \
                   + test_data["language"] + " language"

        # Now change the first answer text direction to left to right

        ex = mySurvey.myQuestion.change_answer_text_direction_to_ltr(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Change text direction in answer field for " +
                                 test_data["language"] + " language",
                                 "Change and verifies that text direction in answer field field is Left for " +
                                 test_data["language"] + " language",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to change and verify that text direction in answer field is Left for  " \
                   + test_data["language"] + " language"

        # Code to resave the question after updating the text direction to LTR
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question saved with LTR language",
                                 "Verified that question saved with LTR language for question title and answer choices",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that question saved with LTR language for question title and answer choice."
        # Code to verify whether the question title saved with text in right to left direction
        mySurvey.myQuestion.click_on_question_to_edit()
        ex = mySurvey.myQuestion.verify_ltr_text_direction_in_question_field()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify text direction(LTR) in question title "
                                                               "field for " + test_data["language"] + " language",
                                 "verifies that text direction in question title field is Left for " +
                                 test_data["language"] + " language",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that text direction in question title field is Left for  " \
                   + test_data["language"] + " language"

        # Code to verify whether the answer choices saved with text in right to left direction

        ex = mySurvey.myQuestion.verify_ltr_text_direction_in_answer_field(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify text direction(LTR) in answer field for " +
                                 test_data["language"] + " language",
                                 "verifies that text direction in answer field field is Left for " +
                                 test_data["language"] + " language",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that text direction in answer field is Left for  " \
                   + test_data["language"] + " language"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
