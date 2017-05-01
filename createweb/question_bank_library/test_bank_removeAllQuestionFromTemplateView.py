from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestBankRemoveAllQuestionFromTemplateView/",  # report_relative_location
                               "test_bank_removeAllQuestionFromTemplateView",  # report_file_name_prefix
                               "Verify remove all Questions from Template View",  # test_suite_title
                               ("Test to verify remove all Questions from Template View"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})

    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

@pytest.mark.MT1
@pytest.mark.C280930
@pytest.mark.IB
@pytest.mark.QBL
def test_bank_removeAllQuestionFromTemplateView(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify remove all Questions from Template View")

    open_category = "AllCategories"

    try:
        mySurvey.myBank.unfold_QuestionBankRegion()
        ex = mySurvey.myQBank.openCategory(open_category)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify open "+ open_category + " Category",
                             "Clicks on " + open_category + " and makes sure that "
                             "it opens with " + open_category + " as hero button",
                             ex,
                             True,
                             not ex,
                             driver)
        assert ex, open_category + " Category closing the modal failed"
        ex = mySurvey.myQBank.checkTopBarRecommendedTemplates()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that top-bar with recommended templates",
                                 "check to make sure that top-bar with recommended templates",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify top-bar with recommended templates"
        ex = mySurvey.myQBank.selectTopBarRecommendedTemplates()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify recommended template click",
                                 "check to make sure that recommened template clicked",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to clicked on recommended template"
        ex = mySurvey.myQBank.verifySelectAllQuestionTemplateBar()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that bar with checkbox, template name",
                                 "check to make sure that bar with checkbox, template name",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify bar with checkbox, template name"
        ex = mySurvey.myQBank.selectAllQuestionCheckbox()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify all question checkbox is selected",
                                 "check to make sure that all question checkbox is selected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify all question checkbox is selected"
        totalQuestions = int(mySurvey.myQBank.getTotalQuestions()) # QBL-200
        ex = mySurvey.myQBank.verifyTotalQuestionAddedInPreview(totalQuestions)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that All questions from the template added "
                                 "to Preview in the right column",
                                 "check to make sure that All questions from the "
                                 "template should then be added to Preview in the right column",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify all questions from the template added to Preview in the right column"
        mySurvey.myQBank.deselectAllQuestionCheckbox()
        ex = mySurvey.myQBank.verifyEmptyQuestionsInPreivew()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that all questions added from "
                                                               "the template are removed ",
                                 "check to make sure that all questions added from the "
                                 "template should then be removed from Preview in the right column",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify remove all questions from Preview in the right column"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
