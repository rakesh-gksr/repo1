from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):

    report = reporting_wrapper("Create",  # report_feature_name
                               "TestStarQTypeSwitchingToDropdown/",  # report_relative_location
                               "test_starQType_switchingToDropdown",  # report_file_name_prefix
                               "verify switching from star to matrix dropdown menu question type, saving them and back "
                               "to star can be saved without an error showing default settings.",  # test_suite_title
                               ("Test to verify switching from star to matrix dropdown menu question type, saving them "
                                "and back to star can be saved without an error showing default settings."),
                               # test_suite_description
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
@pytest.mark.star_question
@pytest.mark.BVT
@pytest.mark.C812408
def test_starQType_switchingToDropdown(create_survey):
    driver, mySurvey, report = create_survey
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test to verify switching from star to matrix dropdown menu "
                                                           "question type, saving them and back to star can be saved "
                                                           "without an error showing default settings.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        # code to add star question to survey
        mySurvey.myBuilder.click_star_rating_add_button()
        mySurvey.myQuestion.enter_question_title('Rate SurveyMonkey services')
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Star question Add to Live Preview",
                                 "Verifies that Star question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Star question added to live preview."
        mySurvey.myQuestion.click_on_question_to_edit()
        # code to change star question type to dropdown textbox
        mySurvey.myQuestion.changeQType("Dropdown")
        ex = mySurvey.myQuestion.verify_question_in_edit_mode('question-single-choice-select')
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify change question type from Star to Dropdown",
                                 "verifies that changed question type from Star to Dropdown",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Dropdown"

        ex = mySurvey.myQuestion.verifySwitchQuestionTypeWarningMsg()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify error message",
                                 "verifies that warning message display while changing the question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify warning message"
        for x in range(1, 4):
            ex = mySurvey.myQuestion.verify_multipleChoice_answerRow_state(True, x)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify empty answer choice",
                                     "Verifies empty answer choice for matrix answer row " + str(x),
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify empty answer choice for matrix answer row " + str(x)
        answerRows = []
        title = mySurvey.myLogic.RNG(30)
        mySurvey.myQuestion.enter_question_title(title)
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, answerRows[2])
        # code to save dropdown text box question type
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify Save Dropdown question type",
                                 "verifies that Dropdown question type saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Dropdown question type saved"
        # code to edit dropdown text box question type
        mySurvey.myQuestion.click_on_question_to_edit()
        # code to change Dropdown textbox question type to star
        mySurvey.myQuestion.changeQType("StarRating")
        ex = mySurvey.myQuestion.verify_question_in_edit_mode('question-emoji-rating')
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify change question type from Dropdown to Star",
                                 "verifies that changed question type from Dropdown to Star",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Star"
        # code to verify star rating question options scale and shape are appear selected or not
        shape = mySurvey.myQuestion.verify_star_rating_question_shape("star")
        scale = mySurvey.myQuestion.verify_star_rating_question_scale("5")
        ex = (shape and scale)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify normal star edit mode with default values shown",
                                 "Verified that star rating question default values showing as expected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star rating question default values showing as expected."
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify Save Star Rating question type",
                                 "verifies that Star Rating question type saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Star Rating question type saved"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
