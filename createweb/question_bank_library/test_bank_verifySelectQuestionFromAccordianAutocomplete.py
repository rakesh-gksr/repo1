from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestBankVerifySelectQuestionFromAccordianAutocomplete/",  # report_relative_location
                               "test_bank_verifySelectQuestionFromAccordianAutocomplete",  # report_file_name_prefix
                               "Verify question selected from Accordion Autocomplete",  # test_suite_title
                               ("Test to verify question selected from Accordion Autocomplete"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})

    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

@pytest.mark.C280914
@pytest.mark.IB
@pytest.mark.QBL
def test_bank_verifySelectQuestionFromAccordianAutocomplete(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify question selected from Accordion Autocomplete")

    try:
        search_keyword = "What"
        mySurvey.myBank.unfold_QuestionBankRegion()
        ex = mySurvey.myQBank.type_autocomplete_search_input_question(search_keyword)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Autocomplete Text Box",
                                 "Check able to enter the autocomplete text in text box",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add autocomplete text in text box"
        ex = mySurvey.myQBank.verifySearchQuestionAutocompleteQuestionList()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question count",
                                 "Check to make sure that there should be max of 5 questions are present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify max of 5 questions are present"
        ex = mySurvey.myQBank.verifySearchQuestionAutocompleteTemplateList()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify templates count",
                                 "Check to make sure that there should be max of 3 templates are present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify max of 3 templates are present"
        ex = mySurvey.myQBank.verifySearchQuestionAutocompleteTagList()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify tags count",
                                 "Check to make sure that there should be max of 3 tags are present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify max of 3 tags are present"

        ex = mySurvey.myQBank.verifyHoverOnAutocompleteResultQuestion()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify autocomplete result question hover color",
                                 "Check to make sure that background color on hover question is light blue",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify light blue color on question hover"

        ex = mySurvey.myQBank.clickOnAutocompleteResultQuestion(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question added in edit mode",
                                 "Check to make sure that question should be added in edit mode",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question added in edit mode"
        mySurvey.myQBank.saveQuestionBankQuestion()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Main survey questions",
                                 "Verify Main survey Questions.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify main survey questions"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
