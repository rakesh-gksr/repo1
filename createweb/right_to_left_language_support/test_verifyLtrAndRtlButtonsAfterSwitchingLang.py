from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from dynamic_tests.dynamic_tests_config import test_data_for_RTL_buttons_verification_after_switching_lang
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):

    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifyLtrAndRtlButtonsAfterSwitchingLang/",  # report_relative_location
                               "test_verifyLtrAndRtlButtonsAfterSwitchingLang",  # report_file_name_prefix
                               ("Verify creating couple of questions with rtl direction with survey language as "
                                "Arabic/Persian/Hebrew. After that switch to language like English and make sure on "
                                "the saved fields with rtl direction an ltr button is displayed to change the "
                                "direction"),  # test_suite_title
                               ("Test to verify creating couple of questions with rtl direction with survey "
                                "language as Arabic/Persian/Hebrew. After that switch to language like English "
                                "and make sure on the saved fields with rtl direction an ltr button is displayed "
                                "to change the direction"),  # test_suite_description
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
@pytest.mark.C7133051
@pytest.mark.C21775200
@pytest.mark.C21775201
@pytest.mark.parametrize("test_data", test_data_for_RTL_buttons_verification_after_switching_lang,
                         ids=[dict['test_rail_id'] for dict in
                              test_data_for_RTL_buttons_verification_after_switching_lang])
def test_verify_ltr_and_rtl_buttons_after_switching_lang(create_survey, test_data):
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

        mySurvey.myOptions.unfold_OptionsRegion()
        mySurvey.myOptions.languageSelect("English", mySurvey)

        mySurvey.myQuestion.click_on_question_to_edit(1)
        ex = mySurvey.myQuestion.check_question_title_rtl_button_inline_editor()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify LTR and RTL buttons for " +
                                 test_data["language"] + " language",
                                 "verifies that ltr and rtl buttons are appears in inline editor of question title",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that ltr and rtl buttons are appears in inline editor of question title"
        mySurvey.myQuestion.open_advanced_editor()
        ex = mySurvey.myQuestion.check_question_title_rtl_button_advanced_editor()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify LTR and RTL buttons for " +
                                 test_data["language"] + " language",
                                 "verifies that ltr and rtl buttons are appears in advanced editor of question title",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that ltr and rtl buttons are appears in inline advanced of question title"

        mySurvey.myQuestion.close_advanced_editor()

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
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
