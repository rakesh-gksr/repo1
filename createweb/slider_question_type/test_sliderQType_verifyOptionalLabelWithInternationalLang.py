#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify optional label with international language

"""

from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest

@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSliderQTypeVerifyOptionalLabelWithInternationalLang/",  # report_relative_location
                               "test_sliderQType_verifyOptionalLabelWithInternationalLang",  # report_file_name_prefix
                               # test_suite_title
                               "verify optional label with international lang",
                               "Test to verify optional label with international lang",  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver

    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().\
        strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

@pytest.mark.skipif(True, reason="skip other option for slider")
@pytest.mark.the_other_slider_option
@pytest.mark.slider_question
@pytest.mark.BVT
@pytest.mark.IB
@pytest.mark.C424127
def test_sliderQType_verifyOptionalLabelWithInternationalLang(create_survey):
    driver, mySurvey, report = create_survey
    test_data = "évalueriez-vous la compétence de l'enseignant(e)"
    test_data = unicode(test_data, errors="ignore")

    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify optional label with international lang")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        ex = mySurvey.myQuestion.turn_on_multichoice_otheroption()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Turn on Other Answer Option",
                                 "Verified that slider question other answer option is turned on",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify slider question other answer option is turned on"
        mySurvey.myQuestion.enter_otheroption_labletext(test_data)
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Slider Question with international language",
                                 "Verified that Slider question with international language characters added to Survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Slider question with international language characters added to Survey"

        ex = mySurvey.myQuestion.verify_other_answer_textbox_text(test_data)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Text Entered With Extended Characters appears ok",
                                 "Verified that text entered with extended characters appears ok on live preview",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify text entered with extended characters appears ok on live preview"


    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
