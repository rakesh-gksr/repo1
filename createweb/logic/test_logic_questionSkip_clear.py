from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicQuestionSkipClear/",  # report_relative_location
                               "test_logic_questionSkip_clear",  # report_file_name_prefix
                               "verify clear all logic , use QB question",  # test_suite_title
                               ("This test adds 3 pages with 2 questions each. Test adds question skip logic  "
                                " and verifies that clear all button clears logic."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_questionSkip_clear(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify clear all logic , use QB question.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        page_num1 = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_multichoice_question_raw(mySurvey.survey_id, page_num1, "Best Kongou Class Ship?", 1,
                                                                  ["Kongou", "Hiei", "Kirishima"])

        mySurvey.myBuilder.click_NewPageAddButton()
        page_num2 = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_multichoice_question_raw(mySurvey.survey_id, page_num2, "Favorite League ADC Champion?",
                                                              1,
                                                              ["Ashe", "Caitlyn", "Corki"])

        mySurvey.myQuestion.generate_multichoice_question_raw(mySurvey.survey_id, page_num2, "This wormhole leads to...",
                                                              2,
                                                              ["A room with a moose", "Fluffy Pillows", "Pixels"])

        mySurvey.myBuilder.click_NewPageAddButton()
        page_num3 = mySurvey.myDesign.getPageID(3)
        mySurvey.myQuestion.generate_multichoice_question_raw(mySurvey.survey_id, page_num3, "Favorite Destroyer?",
                                                              1,
                                                              ["Shimakaze", "Yuudachi", "Amatsukaze"])

        mySurvey.myQuestion.generate_multichoice_question_raw(mySurvey.survey_id, page_num3, "Is this survey becoming silly?",
                                                              2,
                                                              ["Oh yeah", "Nope, nothing to see here", "Maybe, I'm confused"])
        driver.refresh()
        mySurvey.myBank.add_questionBankQuestion_via_qbsvc(
            "How noisy is this neighborhood?", mySurvey.survey_id, page_num1, 2)

        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myQuestion.click_question_logic_tab()
        mySurvey.myLogic.setQuestionSkipLogic(1, 2, False, 3, True)
        mySurvey.myLogic.setQuestionSkipLogic(2, 3, False, 5, True)
        mySurvey.myLogic.setQuestionSkipLogic(3, 1, False)
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myQuestion.click_question_logic_tab()
        ex = mySurvey.myLogic.verify_questionSkipLogic(1, 2, 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question skip logic destination",
                                 "Verifies that question skip logic has the correct destination set.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question skip logic for row 1."
        ex = mySurvey.myLogic.verify_questionSkipLogic(2, 3, 5)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question skip logic destination",
                                 "Verifies that question skip logic has the correct destination set.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question skip logic for row 2."
        ex = mySurvey.myLogic.verify_questionSkipLogic(3, 1, "Top of page")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question skip logic destination",
                                 "Verifies that question skip logic has the correct destination set.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question skip logic for row 3."
        mySurvey.myLogic.clearAll_questionSkipLogic()
        ex = mySurvey.myLogic.verifyQuestionLogicApplied()
        ex = not ex
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question skip logic removed",
                                 "Verifies that question skip logic icon removed.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question skip logic removed."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
