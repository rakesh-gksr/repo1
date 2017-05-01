from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicMultiPageBlock/",  # report_relative_location
                               "test_logic_multiPageBlock",  # report_file_name_prefix
                               # test_suite_title
                               "Verify question logic within a multiple pages block",
                               ("This test adds 8 pages with questions . Test adds question logic with multiple pages blocks "
                                " and verifies that question skip logic works in preview."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

def _setup_questions(mySurvey, driver, report):
    survey_title = mySurvey.myCreate.get_survey_title()
    new_survey_id = mySurvey.myCreate.copy_exiting_survey_via_svysvc("130473859",
                                                          "58310199",
                                                          survey_title + " Copied via svysvc")
    url = mySurvey.myCreate.open_copied_survey(new_survey_id['survey_id'])
    driver.get(url)
    report.add_report_record(ReportMessageTypes.TEST_STEP,
                             "Survey Loaded or recreated",
                             "The survey has either been copied or recreated and is ready for the test",
                             True,
                             True,
                             False,
                             driver)

def test_logic_multiPageBlock_random(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify randomize within block.")
    try:
        _setup_questions(mySurvey, driver, report)
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.click_blockRandom_newBlock()
        mySurvey.myLogic.addSequentialBlocks([1, 2, 3])
        mySurvey.myLogic.addSequentialBlocks([4, 5, 6])
        mySurvey.myLogic.addSequentialBlocks([7, 8])
        mySurvey.myLogic.blockRandomDone()
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.singleBlockLogicSelect(1, "random")
        mySurvey.myLogic.blockRandomDone()
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Open a new survey and click the preview button",
                                 "Opens a new Survey and clicks the preview button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.click_off_preview_warning()
        ex = mySurvey.myDesign.process_multiPage_random_preview(
            [["Best Kongou Class Ship?", "Best Vocaloid?"],
             ["Favorite League ADC Champion?", "This wormhole leads to...",
              "Favorite Destroyer?"],
             ["Favorite League AP Mid Champion?",
              "Is this survey becoming silly?",
              "Favorite editor?(flamewar initiated)"]])
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify randomness of pages in block",
                                 "Verifies that pages are all accessed in random order within block",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify inside block random"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

def test_logic_multiPageBlock_flip(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify flipping within block.")
    try:
        _setup_questions(mySurvey, driver, report)
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.click_blockRandom_newBlock()
        mySurvey.myLogic.addSequentialBlocks([1, 2, 3])
        mySurvey.myLogic.addSequentialBlocks([4, 5, 6])
        mySurvey.myLogic.addSequentialBlocks([7, 8])
        mySurvey.myLogic.blockRandomDone()
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.singleBlockLogicSelect(1, "flip")
        mySurvey.myLogic.blockRandomDone()
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Open a new survey and click the preview button",
                                 "Opens a new Survey and clicks the preview button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.click_off_preview_warning()
        ex = mySurvey.myDesign.process_multiPage_flip_preview(
            [["Best Kongou Class Ship?", "Best Vocaloid?"],
             ["Favorite League ADC Champion?", "This wormhole leads to...",
              "Favorite Destroyer?"],
             ["Favorite League AP Mid Champion?",
              "Is this survey becoming silly?",
              "Favorite editor?(flamewar initiated)"]])
        if not ex:
            numRetries = 10
            while numRetries > 0 and not ex:
                mySurvey.myDesign.return_from_preview_window()
                ex = mySurvey.myDesign.click_preview_button()
                report.add_report_record(ReportMessageTypes.TEST_STEP,
                                         "Open a new survey and click the preview button",
                                         "Opens a new Survey and clicks the preview button.",
                                         ex,
                                         True,
                                         not ex,
                                         driver)
                assert ex, "Failed to click Preview Button"
                ex = mySurvey.myDesign.switch_to_preview_window()
                report.add_report_record(ReportMessageTypes.TEST_STEP,
                                         "Switching Focus to new window opened",
                                         "Switches Focus to what should be the preview and test window.",
                                         ex,
                                         True,
                                         not ex,
                                         driver)
                mySurvey.myDesign.click_off_preview_warning()
                print "retry number " + str(11 - numRetries) + " for flipping check"
                ex = mySurvey.myDesign.process_multiPage_flip_preview(
                    [["Best Kongou Class Ship?", "Best Vocaloid?"],
                     ["Favorite League ADC Champion?", "This wormhole leads to...",
                      "Favorite Destroyer?"],
                     ["Favorite League AP Mid Champion?",
                      "Is this survey becoming silly?",
                      "Favorite editor?(flamewar initiated)"]])
                numRetries -= 1
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify flipped pages in block",
                                 "Verifies that pages are all accessed in flipped order within block",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify inside block flip"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

def test_logic_multiPageBlock_rotate(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify rotating within block.")
    try:
        _setup_questions(mySurvey, driver, report)
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.click_blockRandom_newBlock()
        mySurvey.myLogic.addSequentialBlocks([1, 2, 3])
        mySurvey.myLogic.addSequentialBlocks([4, 5, 6])
        mySurvey.myLogic.addSequentialBlocks([7, 8])
        mySurvey.myLogic.blockRandomDone()
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.singleBlockLogicSelect(1, "rotate")
        mySurvey.myLogic.blockRandomDone()
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Open a new survey and click the preview button",
                                 "Opens a new Survey and clicks the preview button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.click_off_preview_warning()
        ex = mySurvey.myDesign.process_multiPage_rotate_preview(
            [["Best Kongou Class Ship?", "Best Vocaloid?"],
             ["Favorite League ADC Champion?", "This wormhole leads to...",
              "Favorite Destroyer?"],
             ["Favorite League AP Mid Champion?",
              "Is this survey becoming silly?",
              "Favorite editor?(flamewar initiated)"]])
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify rotated pages in block",
                                 "Verifies that pages are all accessed in rotated order within block",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify inside block rotate"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

def test_logic_multiPageBlock_cancelLogic(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Cancel button inside block logic window.")
    try:
        _setup_questions(mySurvey, driver, report)
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.click_blockRandom_newBlock()
        mySurvey.myLogic.addSequentialBlocks([1, 2, 3])
        mySurvey.myLogic.addSequentialBlocks([4, 5, 6])
        mySurvey.myLogic.addSequentialBlocks([7, 8])
        mySurvey.myLogic.blockRandomDone()
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.singleBlockLogicCancel(1, "random")
        ex = mySurvey.myLogic.verifyBlockLogicCancelled(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify logic not added to block",
                                 "Verifies that cancel doesnt add logic to block",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify logic not added to block"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

def test_logic_multiPageBlock_randomSelect(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify randomize within block.")
    try:
        _setup_questions(mySurvey, driver, report)
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.click_blockRandom_newBlock()
        mySurvey.myLogic.addSequentialBlocks([1, 2, 3, 4])
        mySurvey.myLogic.addSequentialBlocks([5, 6])
        mySurvey.myLogic.addSequentialBlocks([7, 8])
        mySurvey.myLogic.blockRandomDone()
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.singleBlockLogicSelect(1, "random", ["P1", "P2", "P3"])
        mySurvey.myLogic.blockRandomDone()
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Open a new survey and click the preview button",
                                 "Opens a new Survey and clicks the preview button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.click_off_preview_warning()
        ex = mySurvey.myDesign.process_multiPage_random_preview(
            [["Best Kongou Class Ship?", "Best Vocaloid?"],
             ["Favorite League ADC Champion?", "This wormhole leads to...",
              "Favorite Destroyer?"],
             ["Favorite League AP Mid Champion?",
              "Is this survey becoming silly?",
              "Favorite editor?(flamewar initiated)"]])
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify randomness of pages in block",
                                 "Verifies that pages are all accessed in random order within block",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify inside block random"
        mySurvey.myDesign.switch_to_preview_iframe()
        ex = mySurvey.myDesign.verify_preview_question_title("Favorite Yamato-Class")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify unselected page in logic now appears last",
                                 "Verifies that page outside logic but inside block appears in static order",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify inside block non logic static page"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

def test_logic_multiPageBlock_flipSelect(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify flipping within block.")
    try:
        _setup_questions(mySurvey, driver, report)
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.click_blockRandom_newBlock()
        mySurvey.myLogic.addSequentialBlocks([1, 2, 3, 4])
        mySurvey.myLogic.addSequentialBlocks([5, 6])
        mySurvey.myLogic.addSequentialBlocks([7, 8])
        mySurvey.myLogic.blockRandomDone()
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.singleBlockLogicSelect(1, "flip", ["P1", "P2", "P3"])
        mySurvey.myLogic.blockRandomDone()
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Open a new survey and click the preview button",
                                 "Opens a new Survey and clicks the preview button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.click_off_preview_warning()
        ex = mySurvey.myDesign.process_multiPage_flip_preview(
            [["Best Kongou Class Ship?", "Best Vocaloid?"],
             ["Favorite League ADC Champion?", "This wormhole leads to...",
              "Favorite Destroyer?"],
             ["Favorite League AP Mid Champion?",
              "Is this survey becoming silly?",
              "Favorite editor?(flamewar initiated)"]])
        if not ex:
            numRetries = 10
            while numRetries > 0 and not ex:
                mySurvey.myDesign.return_from_preview_window()
                ex = mySurvey.myDesign.click_preview_button()
                report.add_report_record(ReportMessageTypes.TEST_STEP,
                                         "Open a new survey and click the preview button",
                                         "Opens a new Survey and clicks the preview button.",
                                         ex,
                                         True,
                                         not ex,
                                         driver)
                assert ex, "Failed to click Preview Button"
                ex = mySurvey.myDesign.switch_to_preview_window()
                report.add_report_record(ReportMessageTypes.TEST_STEP,
                                         "Switching Focus to new window opened",
                                         "Switches Focus to what should be the preview and test window.",
                                         ex,
                                         True,
                                         not ex,
                                         driver)
                mySurvey.myDesign.click_off_preview_warning()
                print "retry number " + str(11 - numRetries) + " for flipping check"
                ex = mySurvey.myDesign.process_multiPage_flip_preview(
                    [["Best Kongou Class Ship?", "Best Vocaloid?"],
                     ["Favorite League ADC Champion?", "This wormhole leads to...",
                      "Favorite Destroyer?"],
                     ["Favorite League AP Mid Champion?",
                      "Is this survey becoming silly?",
                      "Favorite editor?(flamewar initiated)"]])
                numRetries -= 1
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify flipped pages in block",
                                 "Verifies that pages are all accessed in flipped order within block",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify inside block flip"
        mySurvey.myDesign.switch_to_preview_iframe()
        ex = mySurvey.myDesign.verify_preview_question_title(
            "Favorite Yamato-Class")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify unselected page in logic now appears last",
                                 "Verifies that page outside logic but inside block appears in static order",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify inside block non logic static page"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

def test_logic_multiPageBlock_rotateSelect(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify rotating within block.")
    try:
        _setup_questions(mySurvey, driver, report)
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.click_blockRandom_newBlock()
        mySurvey.myLogic.addSequentialBlocks([1, 2, 3, 4])
        mySurvey.myLogic.addSequentialBlocks([5, 6])
        mySurvey.myLogic.addSequentialBlocks([7, 8])
        mySurvey.myLogic.blockRandomDone()
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.singleBlockLogicSelect(1, "rotate", ["P1", "P2", "P3"])
        mySurvey.myLogic.blockRandomDone()
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Open a new survey and click the preview button",
                                 "Opens a new Survey and clicks the preview button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.click_off_preview_warning()
        ex = mySurvey.myDesign.process_multiPage_rotate_preview(
            [["Best Kongou Class Ship?", "Best Vocaloid?"],
             ["Favorite League ADC Champion?", "This wormhole leads to...",
              "Favorite Destroyer?"],
             ["Favorite League AP Mid Champion?",
              "Is this survey becoming silly?",
              "Favorite editor?(flamewar initiated)"]])
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify rotated pages in block",
                                 "Verifies that pages are all accessed in rotated order within block",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify inside block rotate"
        mySurvey.myDesign.switch_to_preview_iframe()
        ex = mySurvey.myDesign.verify_preview_question_title(
            "Favorite Yamato-Class")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify unselected page in logic now appears last",
                                 "Verifies that page outside logic but inside block appears in static order",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify inside block non logic static page"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
