import unittest
from inline_markdown import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):
    # Heading tests
    def test_heading_h1(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h2(self):
        block = "## This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h3(self):
        block = "### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h4(self):
        block = "#### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h5(self):
        block = "##### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h6(self):
        block = "###### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_with_special_chars(self):
        block = "## Heading with **bold** and `code`"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_not_heading_seven_hashes(self):
        block = "####### This is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_heading_no_space(self):
        block = "#This is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_heading_hash_in_middle(self):
        block = "This # is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Code block tests
    def test_code_block_simple(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_multiline(self):
        block = "```\ndef hello():\n    print('world')\n    return True\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_with_language(self):
        block = "```python\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_empty(self):
        block = "```\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_single_backticks(self):
        block = "```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_not_code_block_no_closing(self):
        block = "```\nprint('hello')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_code_block_no_opening(self):
        block = "print('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Quote block tests
    def test_quote_single_line(self):
        block = ">This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_multiple_lines(self):
        block = ">This is a quote\n>with multiple lines\n>all quoted"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_with_space_after_angle(self):
        block = "> This is a quote\n> with spaces"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_with_formatting(self):
        block = ">This is a **bold** quote\n>with _italic_ text"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_not_quote_missing_angle_on_one_line(self):
        block = ">This is a quote\nThis line is not quoted\n>Back to quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_quote_angle_in_middle(self):
        block = "This > is not a quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Unordered list tests
    def test_unordered_list_single_item(self):
        block = "- Item one"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_multiple_items(self):
        block = "- Item one\n- Item two\n- Item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_with_formatting(self):
        block = "- Item with **bold**\n- Item with _italic_\n- Item with `code`"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_long_items(self):
        block = "- This is a really long list item that spans quite a bit\n- Another long item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_not_unordered_list_missing_space(self):
        block = "-Item one\n-Item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_unordered_list_missing_dash_on_one_line(self):
        block = "- Item one\nItem two\n- Item three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_unordered_list_dash_in_middle(self):
        block = "This - is not a list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Ordered list tests
    def test_ordered_list_single_item(self):
        block = "1. First item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_multiple_items(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_with_formatting(self):
        block = "1. Item with **bold**\n2. Item with _italic_\n3. Item with `code`"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_many_items(self):
        block = "1. One\n2. Two\n3. Three\n4. Four\n5. Five\n6. Six\n7. Seven\n8. Eight\n9. Nine\n10. Ten"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_double_digit(self):
        block = "1. First\n2. Second\n3. Third\n4. Fourth\n5. Fifth\n6. Sixth\n7. Seventh\n8. Eighth\n9. Ninth\n10. Tenth\n11. Eleventh"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_not_ordered_list_starts_with_two(self):
        block = "2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_ordered_list_wrong_sequence(self):
        block = "1. First item\n2. Second item\n4. Fourth item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_ordered_list_skips_number(self):
        block = "1. First item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_ordered_list_missing_space(self):
        block = "1.First item\n2.Second item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_ordered_list_missing_period(self):
        block = "1 First item\n2 Second item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_ordered_list_wrong_number_midway(self):
        block = "1. First\n2. Second\n2. Another second\n4. Fourth"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Paragraph tests
    def test_paragraph_simple(self):
        block = "This is just a regular paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_with_formatting(self):
        block = "This paragraph has **bold** and _italic_ text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        block = "This is a paragraph\nthat spans multiple lines\nbut is still a paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_with_special_chars(self):
        block = "This paragraph has special chars: @#$%^&*()"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_with_numbers(self):
        block = "This paragraph mentions 1 and 2 and 3 items"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_with_hash_not_at_start(self):
        block = "This paragraph has a # hashtag"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_empty_string(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Edge cases
    def test_heading_followed_by_text(self):
        block = "# Heading\nSome text below"
        # This should be PARAGRAPH because headings are single-line
        # and we're testing with stripped blocks
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_mixed_list_markers(self):
        block = "- Unordered item\n1. Ordered item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_and_list_mixed(self):
        block = ">Quote line\n- List item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
