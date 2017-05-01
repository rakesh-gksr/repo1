# -*- coding: utf-8 -*-
from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from smsdk.qafw.create.create_start_template import SurveyFromTemplate
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestBankVerifyTemplatesAvailableInPortuguese.py/",  # report_relative_location
                               "test_bank_verifyTemplatesAvailableInPortuguese",  # report_file_name_prefix
                               "Verify Browse Accordion Tiles",  # test_suite_title
                               ("Testing Existance of all Question Bank Categories"),  # test_suite_description
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

@pytest.mark.MT1
@pytest.mark.C280994
@pytest.mark.IB
@pytest.mark.QBL
def test_bank_verifyTemplatesAvailableInPortuguese(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify to see if templates are available in Portuguese")
    try:
        # list of create survey choices
        mySurvey.myCreate.click_new_survey()
        step1 = SurveyFromTemplate(driver)

        ex = step1.verify_create_step1_choices("Start from scratch", "Copy existing survey", "ALL TEMPLATES")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify create step1 3 choices",
                                 "checks to make sure that Build a New Survey from Scratch,"
                                 " Edit a Copy of an Existing Survey, "
                                 "Start from an Expert Template chices are present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify create step1 3 choices"
        ex = mySurvey.myQBank.clickLanguageOnCreateStep1('Português')
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify language change to Portuguese",
                                 "checks to make sure that language changed to Portuguese",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to change language to Portuguese"
        ex = step1.create_survey_from_template()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify expert template option",
                                 "checks to make sure that expert template option is present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click on expert template option"
        ex = step1.verify_create_step1_choices(None, None, "TODOS OS MODELOS")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify portugues template is present",
                                 "checks to make sure that portugues template is present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex,  "Failed to verify portugues template is present"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
    finally:
        mySurvey.myQBank.clickLanguageOnCreateStep1('English')
