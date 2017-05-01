from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from dynamic_tests.dynamic_tests_config import test_data_for_RTL_buttons_verification
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):

    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifyLtrAndRtlButtons/",  # report_relative_location
                               "test_verifyLtrAndRtlButtons",  # report_file_name_prefix
                               "Verify that ltr and rtl buttons appear only when survey language is arabic, "
                               "hebrew or persian(both in inline and in advanced editor)",  # test_suite_title
                               ("Test to verify that ltr and rtl buttons appear only when survey language is arabic, "
                                "hebrew or persian(both in inline and in advanced editor)."),  # test_suite_description
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
@pytest.mark.BVT
@pytest.mark.C7133046
@pytest.mark.C19760467
@pytest.mark.C19760468
@pytest.mark.skipif(True, reason="This is open issue - https://jira.surveymonkey.com/browse/CREATE-7114")
@pytest.mark.parametrize("test_data", test_data_for_RTL_buttons_verification,
                         ids=[dict['test_rail_id'] for dict in test_data_for_RTL_buttons_verification])
def test_verifyLtrAndRtlButtons(create_survey, test_data):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, test_data["test_case_title"])
    try:
        mySurvey.myDesign.modifySurveyTitle("test_RTL Support")
        ex = mySurvey.myDesign.check_rtl_button_in_survey_title()
        ex = not ex
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify LTR and RTL buttons",
                                 "verifies that ltr and rtl buttons are not appears in inline editor of survey title",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that ltr and rtl buttons are not appears in inline editor of survey title"
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin", "Gumi"])
        mySurvey.myQuestion.click_on_question_to_edit(1)
        ex = mySurvey.myQuestion.check_question_title_rtl_button_inline_editor()
        ex = not ex
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify LTR and RTL buttons",
                                 "verifies that ltr and rtl buttons are not appears in inline editor of question title",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that ltr and rtl buttons are not appears in inline editor of question title"
        mySurvey.myQuestion.open_advanced_editor()
        ex = mySurvey.myQuestion.check_question_title_rtl_button_advanced_editor()
        ex = not ex
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify LTR and RTL buttons",
                                 "verifies that ltr and rtl buttons are not appears in advanced editor of question "
                                 "title",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that ltr and rtl buttons are not appears in inline advanced of question title"

        mySurvey.myQuestion.close_advanced_editor()
        mySurvey.myOptions.unfold_OptionsRegion()
        mySurvey.myOptions.languageSelect(test_data["language"], mySurvey)
        ex = mySurvey.myDesign.check_rtl_button_in_survey_title()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify LTR and RTL buttons",
                                 "verifies that ltr and rtl buttons are appears in inline editor of survey title",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that ltr and rtl buttons are appears in inline editor of survey title"
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
        mySurvey.myOptions.unfold_OptionsRegion()
        mySurvey.myOptions.languageSelect("English", mySurvey)
        ex = mySurvey.myDesign.check_rtl_button_in_survey_title()
        ex = not ex
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify LTR and RTL buttons for English Language",
                                 "verifies that ltr and rtl buttons are not appears in inline editor of survey title",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that ltr and rtl buttons are not appears in inline editor of survey title"
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin", "Gumi"])
        mySurvey.myQuestion.click_on_question_to_edit(1)
        ex = mySurvey.myQuestion.check_question_title_rtl_button_inline_editor()
        ex = not ex
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify LTR and RTL buttons for English Language",
                                 "verifies that ltr and rtl buttons are not appears in inline editor of question title",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that ltr and rtl buttons are not appears in inline editor of question title"
        mySurvey.myQuestion.open_advanced_editor()
        ex = mySurvey.myQuestion.check_question_title_rtl_button_advanced_editor()
        ex = not ex
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify LTR and RTL buttons for English Language",
                                 "verifies that ltr and rtl buttons are not appears in advanced editor of question "
                                 "title",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that ltr and rtl buttons are not appears in inline advanced of question title"

        mySurvey.myQuestion.close_advanced_editor()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
