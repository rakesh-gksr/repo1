#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify adding slider question from clicking on 'add a new question button' and then switch to slider.

"""

from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from dynamic_tests.dynamic_tests_config import survey_dict
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSliderQTypeSinglePageMode/",  # report_relative_location
                               "test_sliderQType_singlePageMode",  # report_file_name_prefix
                               # test_suite_title
                               "Copy slider question from page page to another page in single page mode",
                               "Test to copy slider question from page page to another page in single page mode",
                               # test_suite_description
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
@pytest.mark.BVT
@pytest.mark.C83846
def test_sliderQType_singlePageMode_pageSkip(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " set page skip logic on multiple pages in single page mode")
    try:
        survey_title = mySurvey.myCreate.get_survey_title()
        survey_info = survey_dict[pytest.config.option.domain[:3].upper()]["single_page_mode_copy_slider_question"]
        new_survey_id = mySurvey.myCreate.copy_exiting_survey_via_svysvc(survey_info["survey_id"],
                                                              survey_info["user_id"], survey_title +
                                                              " Copied via svysvc")
        url = mySurvey.myCreate.open_copied_survey(new_survey_id['survey_id'])
        driver.get(url)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Survey Loaded or recreated",
                                 "The survey has either been copied or recreated and is ready for the test",
                                 True,
                                 True,
                                 False,
                                 driver)
        ex = mySurvey.myCreate.num_pages_present(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify single page mode",
                                 "checks to make sure that live preview is in single page mode",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify single page mode."
        mySurvey.myCreate.single_page_goto(1)
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P2")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.getCurPage(2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify focus change to Page Skip page",
                                 "checks to make sure that we scroll to the top and are on page 2",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify single page mode."
        mySurvey.myLogic.select_PageSkipTypeDropdown("P3")
        mySurvey.myLogic.click_PageSkipLogicTargetApplyButton()
        ex = mySurvey.myLogic.verify_page_skip_logic_applied(0, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add page skip logic to P1",
                                 "Adds page skip logic to P1 to skip to P2.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add page skip logic from P1 to P2"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.slider_question
@pytest.mark.IB
@pytest.mark.C83847
def test_sliderQType_singlePageMode_questionRandom(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "set slider question randomization on single page mode")
    try:
        survey_title = mySurvey.myCreate.get_survey_title()
        survey_info = survey_dict[pytest.config.option.domain[:3].upper()]["single_page_mode_copy_slider_question"]
        new_survey_id = mySurvey.myCreate.copy_exiting_survey_via_svysvc(survey_info["survey_id"],
                                                              survey_info["user_id"], survey_title +
                                                              " Copied via svysvc")
        url = mySurvey.myCreate.open_copied_survey(new_survey_id['survey_id'])
        driver.get(url)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Survey Loaded or recreated",
                                 "The survey has either been copied or recreated and is ready for the test",
                                 True,
                                 True,
                                 False,
                                 driver)
        mySurvey.myCreate.single_page_goto(1)
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_QuestionRandomization()
        qStack = mySurvey.myLogic.process_singlePageMode_questionRandomization(1)
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
        mySurvey.myDesign.switch_to_preview_iframe()
        ex = mySurvey.myLogic.verify_singlePageMode_QuestionRandomization(10, qStack)
        mySurvey.myDesign.return_from_preview_window()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "verify slider question randomization in preview",
                                 "verifies that all slider questions are randomized in preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify randomness of slider questions"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.slider_question
@pytest.mark.IB
@pytest.mark.C83850
def test_sliderQType_singlePageMode_movePage(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " verify moving page in single page mode")
    try:
        survey_title = mySurvey.myCreate.get_survey_title()
        survey_info = survey_dict[pytest.config.option.domain[:3].upper()]["single_page_mode_copy_slider_question"]
        new_survey_id = mySurvey.myCreate.copy_exiting_survey_via_svysvc(survey_info["survey_id"],
                                                              survey_info["user_id"], survey_title +
                                                              " Copied via svysvc")
        url = mySurvey.myCreate.open_copied_survey(new_survey_id['survey_id'])
        driver.get(url)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Survey Loaded or recreated",
                                 "The survey has either been copied or recreated and is ready for the test",
                                 True,
                                 True,
                                 False,
                                 driver)
        ex = mySurvey.myCreate.num_pages_present(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify single page mode",
                                 "checks to make sure that live preview is in single page mode",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify single page mode."
        mySurvey.myCreate.single_page_goto(1)
        mySurvey.myLogic.movePage(1, 10)  # one is page num in single page mode
        mySurvey.myDesign.scroll_to_top()
        ex = mySurvey.myLogic.getCurPage(10)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify page moved",
                                 "checks to make sure that we moved page to page 10",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify moved page."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.slider_question
@pytest.mark.IB
@pytest.mark.C83851
def test_sliderQType_singlePageMode_pageRandom(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " set page randomization on multiple pages in single page mode")
    try:
        survey_title = mySurvey.myCreate.get_survey_title()
        survey_info = survey_dict[pytest.config.option.domain[:3].upper()]["single_page_mode_copy_slider_question"]
        new_survey_id = mySurvey.myCreate.copy_exiting_survey_via_svysvc(survey_info["survey_id"],
                                                              survey_info["user_id"], survey_title +
                                                              " Copied via svysvc")
        url = mySurvey.myCreate.open_copied_survey(new_survey_id['survey_id'])
        driver.get(url)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Survey Loaded or recreated",
                                 "The survey has either been copied or recreated and is ready for the test",
                                 True,
                                 True,
                                 False,
                                 driver)
        mySurvey.myCreate.single_page_goto(1)
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageRandomization()
        mySurvey.myLogic.pageRandom_randomizePages()
        ex = mySurvey.myLogic.checkPagesRandomizedIcon()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page randomization icon appears",
                                 "checks to make sure that the page randomization icon appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page randomization icon"
        mySurvey.myCreate.single_page_goto(2)
        mySurvey.myLogic.click_PageRandomization()
        mySurvey.myLogic.delete_pageRandomization()
        ex = mySurvey.myLogic.checkPagesRandomizedIcon()
        ex = not ex
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page randomization icon is disabled",
                                 "checks to make sure that the page randomization icon is disabled.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify disabled page randomization icon"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.slider_question
@pytest.mark.IB
@pytest.mark.C83853
def test_sliderQType_singlePageMode_pageBreak(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " verify adding page break in single page mode")
    try:
        survey_title = mySurvey.myCreate.get_survey_title()
        survey_info = survey_dict[pytest.config.option.domain[:3].upper()]["single_page_mode_copy_slider_question"]
        new_survey_id = mySurvey.myCreate.copy_exiting_survey_via_svysvc(survey_info["survey_id"],
                                                              survey_info["user_id"], survey_title +
                                                              " Copied via svysvc")
        url = mySurvey.myCreate.open_copied_survey(new_survey_id['survey_id'])
        driver.get(url)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Survey Loaded or recreated",
                                 "The survey has either been copied or recreated and is ready for the test",
                                 True,
                                 True,
                                 False,
                                 driver)
        ex = mySurvey.myCreate.num_pages_present(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify single page mode",
                                 "checks to make sure that live preview is in single page mode",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify single page mode."
        mySurvey.myCreate.single_page_goto(1)
        mySurvey.myBuilder.unfold_BuilderRegion()
        we = mySurvey.myCreate.get_question('2')
        mySurvey.myBuilder.drag_n_drop_PageBreakButton(we)
        qNum = mySurvey.myCreate.num_questions_in_page(1)
        ex = True if qNum == 1 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verifies page 1 contains only 1 question",
                                 "page break seperated 1 question to current page.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify page break"
        mySurvey.myCreate.single_page_goto(2)
        qNum = mySurvey.myCreate.num_questions_in_page(1)
        ex = True if qNum == 9 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verifies page 2 contains 9 question",
                                 "page break seperated 9 questions to current page.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify page break"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.slider_question
@pytest.mark.IB
@pytest.mark.C83854
def test_singlePageMode_addQuestions(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "add questions to various pages on single page mode survey")
    try:
        survey_title = mySurvey.myCreate.get_survey_title()
        survey_info = survey_dict[pytest.config.option.domain[:3].upper()]["survey_with_249_slider_question"]
        new_survey_id = mySurvey.myCreate.copy_exiting_survey_via_svysvc(survey_info["survey_id"],
                                                              survey_info["user_id"], survey_title +
                                                              " Copied via svysvc")
        url = mySurvey.myCreate.open_copied_survey(new_survey_id['survey_id'])
        driver.get(url)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Survey Loaded or recreated",
                                 "The survey has either been copied or recreated and is ready for the test",
                                 True,
                                 True,
                                 False,
                                 driver)
        ex = mySurvey.myCreate.num_pages_present(1)
        ex = True if ex==False else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify multiple page mode",
                                 "checks to make sure that live preview is in multiple page mode",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify multiple page mode."
        # Code to add new slider question on page no 1
        mySurvey.myCreate.single_page_goto(1)
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Slider question type to survey ",
                                 "Verified that slider question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add slider question to survey."
        # code to verify that new slider question added survey or not. Now total question on page no 1 should be 10
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 11)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question Add to Live Preview",
                                 "Verifies that Slider question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Slider question added to live preview."
        # Code to verify that live preveiw is in multiple page mode
        ex = mySurvey.myCreate.num_pages_present(1)
        ex = True if ex == False else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify multiple page mode",
                                 "checks to make sure that live preview is in multiple page mode",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify multiple page mode."

        # Code to add new slider question on page no 2
        mySurvey.myCreate.single_page_goto(2)
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Slider question type to survey ",
                                 "Verified that slider question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add slider question to survey."
        # code to verify that new slider question added survey or not. Now total question on page no 1 should be 11
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 11)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question Add to Live Preview",
                                 "Verifies that Slider question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Slider question added to live preview."
        # Code to verify that live preveiw is in multiple page mode
        ex = mySurvey.myCreate.num_pages_present(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify single page mode",
                                 "checks to make sure that live preview is in single page mode",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify single page mode."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.slider_question
@pytest.mark.IB
@pytest.mark.C83855
def test_singlePageMode_moveQuestion(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "move questions from one page to another page in single "
                                                           "page mode")
    try:
        survey_title = mySurvey.myCreate.get_survey_title()
        survey_info = survey_dict[pytest.config.option.domain[:3].upper()]["single_page_mode_copy_slider_question"]
        new_survey_id = mySurvey.myCreate.copy_exiting_survey_via_svysvc(survey_info["survey_id"],
                                                              survey_info["user_id"], survey_title +
                                                              " Copied via svysvc")
        url = mySurvey.myCreate.open_copied_survey(new_survey_id['survey_id'])
        driver.get(url)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Survey Loaded or recreated",
                                 "The survey has either been copied or recreated and is ready for the test",
                                 True,
                                 True,
                                 False,
                                 driver)
        mySurvey.myCreate.single_page_goto(2)
        mySurvey.myQuestion.click_on_question_to_edit(1) #26
        title = mySurvey.myQuestion.get_text_of_question_title_in_edit()
        mySurvey.myQuestion.get_text_of_question_title_in_edit()
        mySurvey.myQuestion.click_question_move_tab()
        mySurvey.myLogic.moveQuestionByQuestionIndex(4, 1)

        ex = mySurvey.myLogic.getCurPage(4)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Single Page Mode",
                                 "checks to make sure that we scroll at the top and are on page 4",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify single page mode."
        mySurvey.myQuestion.click_on_question_to_edit(2) #single page mode second question on page
        mySurvey.myQuestion.get_text_of_question_title_in_edit()
        ex = True if mySurvey.myQuestion.get_text_of_question_title_in_edit() == title else False
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question moved",
                                 "checks to make sure that the question was successfully moved from previous page",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify moved question."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.slider_question
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C83856
def test_sliderQType_singlePageMode_copyQuestion(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Copy slider question from page page to another page in "
                                                           "single page mode")
    try:
        survey_title = mySurvey.myCreate.get_survey_title()
        survey_info = survey_dict[pytest.config.option.domain[:3].upper()]["single_page_mode_copy_slider_question"]
        new_survey_id = mySurvey.myCreate.copy_exiting_survey_via_svysvc(survey_info["survey_id"],
                                                              survey_info["user_id"], survey_title +
                                                              " Copied via svysvc")
        url = mySurvey.myCreate.open_copied_survey(new_survey_id['survey_id'])
        driver.get(url)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Survey Loaded or recreated",
                                 "The survey has either been copied or recreated and is ready for the test",
                                 True,
                                 True,
                                 False,
                                 driver)
        mySurvey.myCreate.single_page_goto(1)
        mySurvey.myQuestion.click_on_question_to_edit(1)
        title = mySurvey.myQuestion.get_text_of_question_title_in_edit()
        mySurvey.myQuestion.click_question_copy_tab()
        mySurvey.myLogic.copyQuestion(3, 1)  # becomes new 51
        ex = mySurvey.myLogic.getCurPage(3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Single Page Mode",
                                 "checks to make sure that we scroll at the top and are on page 3",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify single page mode."
        mySurvey.myQuestion.click_on_question_to_edit(2)  # single page mode second question on page
        ex = True if mySurvey.myQuestion.get_text_of_question_title_in_edit() == title else False
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question copied",
                                 "checks to make sure that the question was successfully copied from previous page",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify copied question."
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 11)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question copied on Live Preview",
                                 "Vchecks to make sure that the question was successfully copied from previous page on"
                                 " live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify copied question on live preview."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


