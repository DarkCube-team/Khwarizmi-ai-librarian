import re
from telegram import ReplyKeyboardMarkup


class FilterManager:
    @staticmethod
    def create_filter_keyboard(handler, results):
        filters = handler.get_filters()

        if not filters:
            return None

        keyboard = []

        # First row: Degree level
        if 'مقطع' in filters and filters['مقطع']:
            degree_row = []
            for degree in filters['مقطع'][:3]:  # Maximum 3
                if degree:
                    degree_row.append(f"🎓 {degree}")
            if degree_row:
                keyboard.append(degree_row)

        # Second row: Year (last 5 years)
        if 'سال' in filters and filters['سال']:
            recent_years = filters['سال'][:5]
            if recent_years:
                year_row = [f"📅 {year}" for year in recent_years if year]
                if year_row:
                    keyboard.append(year_row)

        # Third row: General buttons
        keyboard.append(["🔍 فیلتر رشته", "👨‍🏫 فیلتر استاد"])
        keyboard.append(["❌ بدون فیلتر", "🔙 بازگشت"])

        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    @staticmethod
    def parse_filter_from_message(message):
        message_lower = message.lower().strip()
        filters = {}

        # Degree filter
        if 'دکتری' in message_lower or '🎓 دکتری' in message:
            filters['مقطع'] = 'دکتری'
        elif 'کارشناسی ارشد' in message_lower or '🎓 کارشناسی ارشد' in message:
            filters['مقطع'] = 'کارشناسی ارشد'
        elif 'کارشناسی' in message_lower and 'ارشد' not in message_lower:
            filters['مقطع'] = 'کارشناسی'

        # Year filter
        year_match = re.search(r'(\d{4})', message)
        if year_match:
            filters['سال'] = year_match.group(1)

        # No filter
        if 'بدون فیلتر' in message or '❌' in message:
            return {}

        return filters if filters else None

    @staticmethod
    def is_filter_request(message):
        message_lower = message.lower()

        filter_keywords = [
            'فیلتر', 'فیلتر کن', 'محدود کن',
            '🎓', '📅', '🔍', '👨‍🏫',
            'مقطع', 'سال', 'رشته', 'استاد',
            'دکتری', 'کارشناسی', 'ارشد'
        ]

        return any(keyword in message_lower or keyword in message for keyword in filter_keywords)

    @staticmethod
    def create_field_filter_keyboard(field_type, options):
        keyboard = []

        # Display maximum 10 top options
        top_options = options[:10]

        # Divide into rows of 2
        for i in range(0, len(top_options), 2):
            row = top_options[i:i + 2]
            keyboard.append(row)

        # Control buttons
        keyboard.append(["❌ لغو", "🔙 بازگشت"])

        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    @staticmethod
    def format_filter_summary(filters):
        if not filters:
            return "بدون فیلتر"

        parts = []

        if 'مقطع' in filters:
            parts.append(f"مقطع: {filters['مقطع']}")

        if 'سال' in filters:
            parts.append(f"سال: {filters['سال']}")

        if 'رشته' in filters:
            parts.append(f"رشته: {filters['رشته']}")

        if 'استاد راهنما' in filters:
            parts.append(f"استاد: {filters['استاد راهنما']}")

        return " | ".join(parts)
