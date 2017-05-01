from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from dynamic_tests.dynamic_tests_config import test_data_for_RTL_text_direction, input_data_for_RTL_text_direction
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):

    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifyTextDirection/",  # report_relative_location
                               "test_verifyTextDirection",  # report_file_name_prefix
                               "Verify that for a new edit question title/answer option, etc the default language "
                               "is rtl for the above mentioned languages.",  # test_suite_title
                               ("Test to Verify that for a new edit question title/answer option, etc the "
                                "default language is rtl for the above mentioned languages."),  # test_suite_description
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
@pytest.mark.C7133048
@pytest.mark.C19980458
@pytest.mark.C19980459
@pytest.mark.parametrize("test_data", test_data_for_RTL_text_direction,
                         ids=[dict['test_rail_id'] for dict in test_data_for_RTL_text_direction])
@pytest.mark.parametrize("input_data", input_data_for_RTL_text_direction,
                         ids=[dict['input_type'] for dict in input_data_for_RTL_text_direction])
def test_verify_text_direction(create_survey, test_data, input_data):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, test_data["test_case_title"])
    try:
        mySurvey.myDesign.modifySurveyTitle("test_RTL Support")
        mySurvey.myOptions.unfold_OptionsRegion()
        mySurvey.myOptions.languageSelect(test_data["language"], mySurvey)
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        ex = mySurvey.myQuestion.verify_rtl_text_direction_in_question_field(input_data["question_title"])
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

        ex = mySurvey.myQuestion.verify_rtl_text_direction_in_answer_field(1, input_data["answer_choice_title"])
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

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
