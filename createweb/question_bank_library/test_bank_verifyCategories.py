from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestBankVerifyCategories/",  # report_relative_location
                               "test_bank_verifyCategories",  # report_file_name_prefix
                               "Verify Browse Accordion Tiles",  # test_suite_title
                               ("Testing Existance of all Question Bank Categories"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})

    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

category_list = [
    {'category': "PreviouslyUsedQuestions",
     'category_name': "Previously Used"},
    {'category': "AllCategories",
     'category_name': "All Categories"},
    {'category': "Community",
     'category_name': "Community"},
    {'category': "Demographics",
     'category_name': "Demographics"},
    {'category': "CustomerFeedback",
     'category_name': "Customer Feedback"},
    {'category': "CustomerSatisfaction",
     'category_name': "Customer Satisfaction"},
    {'category': "Education",
     'category_name': "Education"},
    {'category': "Events",
     'category_name': "Events"},
    {'category': "Healthcare",
     'category_name': "Healthcare"},
    {'category': "JustForFun",
     'category_name': "Just for Fun"},
    {'category': "HumanResources",
     'category_name': "Human Resources"},
    {'category': "IndustrySpecific",
     'category_name': "Industry Specific"},
    {'category': "MarketResearch",
     'category_name': "Market Research"},
    {'category': "Non-Profit",
     'category_name': "Non-Profit"},
    {'category': "Political",
     'category_name': "Political"},
]


@pytest.mark.C280961
@pytest.mark.C292410
@pytest.mark.IB
@pytest.mark.QBL
@pytest.mark.parametrize("category_check", category_list, ids=[dict['category_name'] for dict in category_list])
def test_bank_verify_categories(create_survey, category_check):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verifying Existance of all Question Bank Categories")
    try:
        mySurvey.myBank.unfold_QuestionBankRegion()
        # for category in category_list:
        ex = mySurvey.myQBank.verifyCategoryExists(category_check["category"], category_check['category_name'])
        if not ex:
            ex = mySurvey.myQBank.verifyCategoryExists(
                category_check["category"], category_check['category_name'])  # retry due to error from loading QB
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify " + category_check['category_name'] + " category",
                                 "Clicks on " + category_check['category_name'] + " and makes sure that "
                                 "it opens with " + category_check['category_name'] + " as hero button",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, category_check["category"] + " Category verification failure"
        ex = mySurvey.myQBank.closeCategory()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify close " + category_check['category_name'] + " Category",
                                 "Clicks on close button to close the modal ",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, category_check["category"] + " Category closing the modal failed"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
