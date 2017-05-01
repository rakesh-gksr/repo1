from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from dynamic_tests.dynamic_tests_config import test_data_for_placeholder_verification
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):

    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifyPlaceholder/",  # report_relative_location
                               "test_verifyPlaceholder",  # report_file_name_prefix
                               "Verify the placeholder text getting removed for the input fields as soon as the text "
                               "is typed in the field.",  # test_suite_title
                               ("Test to verify the placeholder text getting removed for the input fields as "
                                "soon as the text is typed in the field."),  # test_suite_description
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
@pytest.mark.C16892850
@pytest.mark.C23677687
@pytest.mark.C23677688
@pytest.mark.parametrize("test_data", test_data_for_placeholder_verification,
                         ids=[dict['test_rail_id'] for dict in test_data_for_placeholder_verification])
def test_verify_text_direction(create_survey, test_data):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, test_data["test_case_title"])
    try:
        mySurvey.myOptions.unfold_OptionsRegion()
        mySurvey.myOptions.languageSelect(test_data["language"], mySurvey)
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        ex = mySurvey.myQuestion.verify_placeholder_text_before_typing_in_question_field()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify placeholder text before typing in question "
                                                               "title field for " + test_data["language"] + " language",
                                 "verifies that placeholder text is showing in question field before typing question "
                                 "title for " + test_data["language"] + " language",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that placeholder text is showing in question field before typing question title " \
                   "for  " + test_data["language"] + " language"
        ex = mySurvey.myQuestion.verify_placeholder_text_after_typing_in_question_field("Please classify the following Ships")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify placeholder text after typing in question "
                                                               "title field for " + test_data["language"] + " language",
                                 "verifies that placeholder text is showing in question field after typing question "
                                 "title for " + test_data["language"] + " language",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that placeholder text is showing in question field after typing question title " \
                   "for  " + test_data["language"] + " language"
        ex = mySurvey.myQuestion.verify_placeholder_text_before_typing_in_answer_field(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify placeholder text before typing in answer "
                                                               "field for " + test_data["language"] + " language",
                                 "verifies that placeholder text is showing in answer field before typing answer "
                                 "option for " + test_data["language"] + " language",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that placeholder text is showing in answer field for  " \
                   + test_data["language"] + " language"

        ex = mySurvey.myQuestion.verify_placeholder_text_after_typing_in_answer_field(1, "Haruna")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify placeholder text after typing in answer "
                                                               "field for " + test_data["language"] + " language",
                                 "verifies that placeholder text is showing in answer field after typing answer "
                                 "option for " + test_data["language"] + " language",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that placeholder text is showing in answer field for" + \
                   test_data["language"] + " language"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
