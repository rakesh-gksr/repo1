from smsdk.qafw.create.create_utils import reporting_wrapper, env_init, reload_page, wait_Accordion_Ready
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAccountsMonthlyFeatures/",  # report_relative_location
                               "test_accounts_monthlyFeatures",  # report_file_name_prefix
                               "Verify Select Monthly Account Features and Upgrades",  # test_suite_title
                               ("This test adds all upgrade features to a survey "
                                " and then verifies usage notification."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init('MONTHLY')
    import datetime
    import os

    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime(
        "%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()

    request.addfinalizer(fin)
    return report, testcasename


def test_accounts_monthlyVerifyAll(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test all features that Select Monthly Account can use.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        for x in xrange(11):
            mySurvey.myQuestion.generate_multichoice_question_raw(mySurvey.survey_id, page_num, "Best KanMusu?", x + 1,
                                                          ["Haruna", "Kongou", "Yuudachi"])
        reload_page(driver)
        wait_Accordion_Ready(driver)
        mySurvey.myDesign.clickNextButton()
        ex = mySurvey.myDesign.verifyCollectorPage()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "More than 10 Questions feature",
                                 "Verifies Gold user can add more than 10 questions to a survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify >10 questions feature."
        mySurvey.myDesign.click_designSurvey_tab()
        mySurvey.myQuestion.generate_menu_matrix_question(
            mySurvey.survey_id, page_num,
            "Best Vocaloid?", 12)
        mySurvey.myDesign.clickNextButton()
        ex = mySurvey.myDesign.verifyCollectorPage()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Menu Matrix question type feature",
                                 "Verifies Gold user can add menu matrix question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify ability to add menu matrix question type."
        mySurvey.myDesign.click_designSurvey_tab()
        mySurvey.myDesign.scroll_to_top()
        mySurvey.myDesign.scroll_to_top()
        mySurvey.myDesign.click_add_logo()
        mySurvey.myDesign.click_upload_logo()
        mySurvey.myDesign.clickNextButton()
        ex = mySurvey.myDesign.verifyCollectorPage()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Logo feature",
                                 "Verifies gold user can add Logo",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Logo feature."
        mySurvey.myDesign.click_designSurvey_tab()
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        mySurvey.myLogic.select_PageSkipTypeDropdown("Disqualify Respondent")
        mySurvey.myLogic.click_PageSkipLogicTargetApplyButton()
        mySurvey.myDesign.clickNextButton()
        ex = mySurvey.myDesign.verifyCollectorPage()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify page skip logic",
                                 "verifies gold user can add page skip logic",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify page skip logic feature."
        mySurvey.myDesign.click_designSurvey_tab()
        mySurvey.myDesign.scroll_to_top()
        mySurvey.myQuestion.click_on_question_to_edit()
        mySurvey.myQuestion.click_question_logic_tab()
        mySurvey.myLogic.setQuestionSkipLogic(1, "End of survey", True)
        mySurvey.myDesign.clickNextButton()
        ex = mySurvey.myDesign.verifyCollectorPage()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question skip logic feature",
                                 "verifies gold user can add question skip logic",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question skip logic feature."
        mySurvey.myDesign.click_designSurvey_tab()
        mySurvey.myTheme.unfold_ThemeRegion()
        mySurvey.myTheme.createNewCustomTheme("testCustomTheme")
        mySurvey.myDesign.clickNextButton()
        ex = mySurvey.myDesign.verifyCollectorPage()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify custom theme feature",
                                 "verifies gold user can add custom theme feature",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify custom theme feature."
        mySurvey.myDesign.click_designSurvey_tab()
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_logicButtonUpgrade("CustomVariables")
        ex = mySurvey.myLogic.verify_upgradeNotify("CustomVariables")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify upgrade notification for custom variables",
                                 "Checks upgrade notification after adding custom variables",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify upgrade notification for custom variables."
        mySurvey.myLogic.close_upgradeNotify("CustomVariables")
        mySurvey.myLogic.click_logicButtonUpgrade("BlockRandom")
        ex = mySurvey.myLogic.verify_upgradeNotify("BlockRandom")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify upgrade notification for block randomization",
                                 "Checks upgrade notification after adding block randomization",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify upgrade notification for block randomization."
        mySurvey.myLogic.close_upgradeNotify("BlockRandom")
        mySurvey.myOptions.unfold_OptionsRegion()
        mySurvey.myLogic.click_logicButtonUpgrade("Footer")
        ex = mySurvey.myLogic.verify_upgradeNotify("Footer")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify upgrade notification for footer removal",
                                 "Checks upgrade notification after removing footer",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify upgrade notification for footer removal."
        mySurvey.myLogic.close_upgradeNotify("Footer")
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myLogic.click_logicButtonUpgrade("RandomAssignment", "text")
        ex = mySurvey.myLogic.verify_upgradeNotify("RandomAssignment")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify upgrade notification for text A/B Test feature",
                                 "verifies select user gets upgrade notification for text A/B Test type question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify upgrade notification for text A/B Test."
        mySurvey.myLogic.close_upgradeNotify("RandomAssignment")
        mySurvey.myLogic.click_logicButtonUpgrade("RandomAssignment", "image")
        ex = mySurvey.myLogic.verify_upgradeNotify("RandomAssignment")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify upgrade notification for image A/B Test feature",
                                 "verifies select user gets upgrade notification for image A/B Test type question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify upgrade notification for image A/B Test."
        mySurvey.myLogic.close_upgradeNotify("RandomAssignment")
        mySurvey.myDesign.scroll_to_top()
        mySurvey.myQuestion.click_on_question_to_edit()
        mySurvey.myQuestion.click_question_options_tab()
        mySurvey.myQuestion.toggleQuestionABTest_upgrade()
        ex = mySurvey.myLogic.verify_upgradeNotify("RandomAssignment")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify upgrade notification for question A/B Test feature",
                                 "verifies select user gets upgrade notification for question A/B Test type question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify upgrade notification for question A/B Test."
        mySurvey.myLogic.close_upgradeNotify("RandomAssignment")
        mySurvey.myQuestion.click_question_edit_tab()
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Haruna")
        mySurvey.myQuestion.addPipingtoQuestion(4)
        ex = mySurvey.myLogic.verify_upgradeNotify("Piping")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify upgrade notification for piping feature",
                                 "verifies select user gets upgrade notification for piping a question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify upgrade notification for question piping."
        mySurvey.myLogic.close_upgradeNotify("Piping")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_logicButtonUpgrade("PageRandom")
        ex = mySurvey.myLogic.verify_upgradeNotify("PageRandom")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify upgrade notification for page randomization",
                                 "Checks upgrade notification after adding page randomization",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify upgrade notification for page randomization."
        mySurvey.myLogic.close_upgradeNotify("PageRandom")
        mySurvey.myLogic.click_logicButtonUpgrade("QuestionRandom")
        ex = mySurvey.myLogic.verify_upgradeNotify("QuestionRandom")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify upgrade notification for question randomization",
                                 "Checks upgrade notification after adding question randomization",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify upgrade notification for question randomization."
        mySurvey.myLogic.close_upgradeNotify("QuestionRandom")
        mySurvey.myLogic.click_logicButtonUpgrade("Quotas")
        ex = mySurvey.myLogic.verify_upgradeNotify("Quotas")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify upgrade notification for quotas",
                                 "Checks upgrade notification after adding quotas",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify upgrade notification for quotas."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()