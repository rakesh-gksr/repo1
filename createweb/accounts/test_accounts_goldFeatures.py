from smsdk.qafw.create.create_utils import reporting_wrapper, env_init, reload_page, wait_Accordion_Ready
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAccountsGoldFeatures/",  # report_relative_location
                               "test_accounts_goldFeatures",  # report_file_name_prefix
                               "Verify Gold Account Features and Upgrades",  # test_suite_title
                               ("This test adds all upgrade features to a survey "
                                " and then verifies usage notification."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init('GOLD')
    import datetime
    import os

    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime(
        "%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()

    request.addfinalizer(fin)
    return report, testcasename


def test_accounts_verifyAll(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test all features that Gold Account can use.")
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
        mySurvey.myBuilder.click_ImageABTestAddButton()
        mySurvey.myQuestion.enter_imageAB_url(1,
                                              "http://images5.fanpop.com/image/photos/31100000/"
                                              "Keep-Calm-and-Continue-Testing-portal-2-31140076-453-700.jpg")
        mySurvey.myQuestion.enter_imageAB_url(2,
                                              "http://images4.fanpop.com/image/photos/21200000"
                                              "/TACOS-gir-21208550-838-953.jpg")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myDesign.clickNextButton()
        ex = mySurvey.myDesign.verifyCollectorPage()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify image A/B Test feature",
                                 "verifies gold user can add image A/B Test type question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify ability to add image A/B Test."
        mySurvey.myDesign.click_designSurvey_tab()
        mySurvey.myBuilder.click_TextABTestAddButton()
        mySurvey.myQuestion.enter_textAB_textbox(1, mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.enter_textAB_textbox(2, mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myDesign.clickNextButton()
        ex = mySurvey.myDesign.verifyCollectorPage()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify text A/B Test feature",
                                 "verifies Gold user can add text A/B Test type question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify ability to add text A/B Test."
        mySurvey.myDesign.click_designSurvey_tab()
        mySurvey.myDesign.scroll_to_top()
        mySurvey.myQuestion.click_on_question_to_edit()
        mySurvey.myQuestion.click_question_options_tab()
        mySurvey.myQuestion.toggleQuestionABTest()
        mySurvey.myQuestion.editQuestionABTest(mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myDesign.clickNextButton()
        ex = mySurvey.myDesign.verifyCollectorPage()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question A/B Test feature",
                                 "verifies gold user can add question with A/B Test",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question A/B Test feature."
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
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best KanMusu?", 1,
                                                          ["Haruna", "Kongou", "Yuudachi"])
        mySurvey.myQuestion.click_on_question_to_edit(15)
        mySurvey.myQuestion.addPipingtoQuestion(4)
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myDesign.clickNextButton()
        ex = mySurvey.myDesign.verifyCollectorPage()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify piping feature",
                                 "verifies gold user can add piping feature",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify piping feature."
        mySurvey.myDesign.click_designSurvey_tab()
        mySurvey.myQuestion.hover_on_question_to_delete_it(14)
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
        mySurvey.myLogic.click_PageRandomization()
        mySurvey.myLogic.pageRandom_randomizePages()
        mySurvey.myDesign.clickNextButton()
        ex = mySurvey.myDesign.verifyCollectorPage()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify page randomization feature",
                                 "verifies gold user can add page randomization",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify page randomization feature."
        mySurvey.myDesign.click_designSurvey_tab()
        mySurvey.myLogic.click_QuestionRandomization()
        mySurvey.myLogic.questionRandom_randomQuestions(1)
        mySurvey.myDesign.clickNextButton()
        ex = mySurvey.myDesign.verifyCollectorPage()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question randomization feature",
                                 "verifies gold user can add question randomization",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question randomization feature."
        mySurvey.myDesign.click_designSurvey_tab()
        mySurvey.myLogic.click_Quota()
        mySurvey.myLogic.quotaSetupWizard("simple", 1, 1, [1])
        mySurvey.myLogic.click_QuotaDone()
        mySurvey.myDesign.clickNextButton()
        ex = mySurvey.myDesign.verifyCollectorPage()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify quota feature",
                                 "verifies gold user can add quota",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify quota feature."
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
        # Code to add custom variable to survey
        mySurvey.myLogic.click_CustomVarsButton()
        mySurvey.myLogic.enter_CustomVarName()
        mySurvey.myLogic.enter_CustomVarLabel(mySurvey.myLogic.RNG(250))
        mySurvey.myLogic.click_CustomVarNextButton()
        mySurvey.myLogic.click_QuotaFirstDoneButton()
        ex = mySurvey.myLogic.verify_custom_variable_on()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Custom Variable is On",
                                 "Checks custom variable toggle on after adding a custom variable",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify custom variable toggle on after adding a custom variable."
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
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()