# -*- coding: utf-8 -*-
from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestBankVerifyCategoriesInSpanish/",  # report_relative_location
                               "test_bank_verifyCategoriesInSpanish",  # report_file_name_prefix
                               "Verify Browse Accordion Tiles in Spanish (es)",  # test_suite_title
                               ("Testing Existance of all Question Bank Categories in Spanish (es)"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})

    env_init("platinum_default_intl")
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
    {'category': "Demographics",
     'category_name': "Demografía"},
    {'category': "Community",
     'category_name': "Comunidad"},
    {'category': "Education",
     'category_name': "Educación"},
    {'category': "Events",
     'category_name': "Eventos"},
    {'category': "IndustrySpecific",
     'category_name': "Industria específica"},
    {'category': "MarketResearch",
     'category_name': "Investigación de mercado"},
    {'category': "HumanResources",
     'category_name': "Recursos humanos"},
]

languageName = "Spanish"

@pytest.mark.C280991
@pytest.mark.IB
@pytest.mark.QBL
def test_bank_verify_categories_in_spanish(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify Browse Accordion Tiles in Spanish (es)")
    try:
        mySurvey.myOptions.unfold_OptionsRegion()
        ex = mySurvey.myLogic.selectLanguage(languageName)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify language changes to " + languageName,
                                 "check to make sure that language changed to " + languageName,
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, " Failed to change the language to " + languageName
        mySurvey.myBank.unfold_QuestionBankRegion()
        for category in category_list:
            ex = mySurvey.myQBank.verifyCategoryExists(category['category'], category['category_name'], 'Spanish')
            if not ex:
                ex = mySurvey.myQBank.verifyCategoryExists(
                    category['category'], category['category_name'], 'Spanish')  # retry due to error from loading QB
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify " + category['category'] + " category",
                                     "Clicks on " + category['category'] + " and makes sure that "
                                     "it opens with " + category['category'] + " as hero button",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, category['category'] + " Category verification failure"
            ex = mySurvey.myQBank.closeCategory()
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify close "+ category['category'] + " Category",
                                     "Clicks on close button to close the modal ",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, category['category'] + " Category closing the modal failed"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
