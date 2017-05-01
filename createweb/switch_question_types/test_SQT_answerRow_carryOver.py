from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):

    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSQTAnswerRowCarryOver/",  # report_relative_location
                               "test_SQT_answerRow_carryOver",  # report_file_name_prefix
                               "Verifies CREATE-5127 "
                               "Verifies Question Switch State following a question type switch",  # test_suite_title
                               ("This test suite adds a question and performs switching  "
                                " Test verifies answer rows from switched question does not carry over to newly added question."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_SQT_answerRow_carryOver(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verifies CREATE-5127")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        title = mySurvey.myLogic.RNG(30)
        answerRows = []
        mySurvey.myQuestion.enter_question_title(title)
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.changeQType("SingleTextbox")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["TextBox"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to SingleTextbox",
                                 "verifies that the state of the question remains switching to SingleTextbox",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to SingleTextbox"
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        ex = mySurvey.myQuestion.verify_multipleChoice_answerText_empty(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify answer rows didn't carry over from switched question, row 1",
                                 "verifies that the state of the previously switched question type question did not carry to the new question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state of new question, row 1"
        ex = mySurvey.myQuestion.verify_multipleChoice_answerText_empty(2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify answer rows didn't carry over from switched question, row 2",
                                 "verifies that the state of the previously switched question type question did not carry to the new question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state of new question, row 2"
        ex = mySurvey.myQuestion.verify_multipleChoice_answerText_empty(3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify answer rows didn't carry over from switched question, row 3",
                                 "verifies that the state of the previously switched question type question did not carry to the new question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state of new question, row 3 "
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
