#!/usr/bin/env python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verify randomizing slider question from question randomization.

"""

from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest

SliderQuesTitle = "Slider Question"


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestsliderQTypeVerifyQuesRandomization/",  # report_relative_location
                               "test_sliderQType_verifyQuesRandomization",  # report_file_name_prefix
                               # test_suite_title
                               ("verify autosaving slider question from clicking on another question on the survey "
                                "page"),
                               ("Test to verify autosaving slider question from clicking on another question on the "
                                "survey page"),  # test_suite_description
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


@pytest.mark.slider_question
@pytest.mark.IB
@pytest.mark.C284120
def test_sliderQType_verifyQuesRandomization(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify randomizing slider question from question randomization.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myQuestion.generate_matrix_scale_question(mySurvey.survey_id, page_num,
                                                           "Please classify the following Ships", 1,
                                                           ["Haruna", "Yuudachi", "Naka"],
                                                           ["Destroyer(DD)", "Light Cruiser(CL)", "Battleship(BB)",
                                                            "Aircraft Carrier(CV)", "Submarine(SS)"])
        mySurvey.myLogic.pushQuestionToStack("Please classify the following Ships")
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best KanMusu?", 1,
                                                      ["Haruna", "Kongou", "Yuudachi"])
        mySurvey.myLogic.pushQuestionToStack("Best KanMusu?")
        mySurvey.myQuestion.generate_single_textbox_question(mySurvey.survey_id, page_num, "Single Textbox", 1, False)
        mySurvey.myLogic.pushQuestionToStack("Single Textbox")
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title(SliderQuesTitle)
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myLogic.pushQuestionToStack(SliderQuesTitle)
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_QuestionRandomization()
        mySurvey.myLogic.questionRandom_randomQuestions('1: Page 1')
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
        for y in xrange(3):
            if y > 0:
                mySurvey.myDesign.click_preview_button()
                mySurvey.myDesign.switch_to_preview_window()
            for x in xrange(4):
                if x > 0:
                    mySurvey.myDesign.switch_to_preview_window()

                mySurvey.myDesign.switch_to_preview_iframe()
                ex = mySurvey.myLogic.verifyPreviewPageRandomQuestions(x)
                report.add_report_record(ReportMessageTypes.TEST_STEP,
                                         "Successfully Verified question " + str(x + 1) + " pass # " + str(y + 1),
                                         "Sucessfully verified that this question is randomized.",
                                         ex,
                                         True,
                                         not ex,
                                         driver)
                assert ex, "Preview Page Verification failure"
                if x == 3:
                    mySurvey.myDesign.return_from_preview_window()
        ex = mySurvey.myLogic.checkForRandomness(4)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Successfully verified question randomization ",
                                 "Verifies that all questions were all randomized",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify randomization of questions"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
