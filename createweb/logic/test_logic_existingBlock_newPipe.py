from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicExistingBlockNewPipe/",  # report_relative_location
                               "test_logic_existingBlock_newPipe",  # report_file_name_prefix
                               "verify inserting piping within a block",  # test_suite_title
                               ("This test adds pages 1 and 2 to a block "
                                " and then pipes question 1 to question 2"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_existingBlock_newPipe(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify inserting piping within a block.")
    try:
        # page1

        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "How noisy is this neighborhood?")
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()
        ex = mySurvey.myBuilder.click_MultipleChoiceAddButton()
        # time.sleep(3)
        ex = mySurvey.myQuestion.enter_question_title("Best Vocaloid?")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Miku")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Luka")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Rin")
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.click_blockRandom_newBlock()
        mySurvey.myLogic.addSequentialBlocks([1, 2])
        mySurvey.myLogic.blockRandomDone()
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myQuestion.addPipingtoQuestion(1)
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        # time.sleep(1)
        ex = mySurvey.myQuestion.verify_question_piping(2, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify piping",
                                 "checks to make sure that Question 1 is piping into Question 2.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify piping"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
