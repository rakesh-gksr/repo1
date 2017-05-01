from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicQuestionRandom_multiple/",  # report_relative_location
                               "test_logic_questionRandom_multiple",  # report_file_name_prefix
                               "verify randomizing all questions on a selected pages",  # test_suite_title
                               ("This test applies page logic "
                                " question randomization and as a random chance "
                                " to randomize the survey questions on each page."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os

    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime(
        "%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()

    request.addfinalizer(fin)
    return report, testcasename


def test_logic_questionRandom_multiple(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify randomizing all questions on a selected pages.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        page1 = []
        page2 = []
        for x in xrange(10):
            if x == 5:
                mySurvey.myBuilder.click_NewPageAddButton()
            mySurvey.myBuilder.click_MultipleChoiceAddButton()
            randomStringTitle = mySurvey.myLogic.RNG(30)
            mySurvey.myQuestion.enter_question_title(randomStringTitle)
            mySurvey.myQuestion.enter_multipleChoice_answerText(1, mySurvey.myLogic.RNG(10))
            mySurvey.myQuestion.click_question_save_from_edit_tab()
            if x < 5:
                page1.append(randomStringTitle)
            elif x >= 5:
                page2.append(randomStringTitle)
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_QuestionRandomization()
        mySurvey.myLogic.questionRandom_randomQuestions(1)
        ex = mySurvey.myLogic.checkQuestionsRandomizedIcon()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that Question randomization icon appears",
                                 "checks to make sure that the Question randomization icon appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of Question randomization icon"
        mySurvey.myLogic.click_QuestionRandomization()
        mySurvey.myLogic.click_newQuestionRandom()
        mySurvey.myLogic.questionRandom_randomQuestions(2)
        ex = mySurvey.myLogic.checkQuestionsRandomizedIcon()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that Question randomization icon appears",
                                 "checks to make sure that the Question randomization icon appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of Question randomization icon"
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Open a new survey and click the preview button",
                                 "Opens a new Survey and clicks the preview button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.click_off_preview_warning()
        it = []
        for x in xrange(3):
            if x > 0:
                mySurvey.myDesign.click_preview_button()
                mySurvey.myDesign.switch_to_preview_window()
            mySurvey.myDesign.switch_to_preview_iframe()
            it.append(mySurvey.myLogic.verify_multiple_question_randomization([page1, page2]))
            mySurvey.myDesign.return_from_preview_window()
        ex = mySurvey.myLogic.check_for_multi_randomness(it)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Successfully verified question randomization ",
                                 "Verifies that all questions were all randomized",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify randomization of questions"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
