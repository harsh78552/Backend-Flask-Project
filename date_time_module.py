from datetime import datetime, timedelta, date
from Library_Backend_Api.Data_Base.borrow_books import BorrowBook


def get_today_date():
	today_date_ = date.today()
	today__date = today_date_.strftime("%d %B %Y")
	return today__date


def date_after_15_days():
	today_date = get_today_date()
	todaydate_date = datetime.strptime(today_date, "%d %B %Y")
	day15 = todaydate_date + timedelta(days=15)
	result_date = day15.strftime("%d %B %Y")
	return result_date


class TotalDate:
	def __init__(self):
		self.borrow_book_data_ = BorrowBook()

	def total_date(self):
		issue_data = self.borrow_book_data_.get_borrow_book_data()
		date1 = datetime.strptime(issue_data[0]['borrow_date'], "%Y-%m-%d")
		date2 = datetime.strptime(get_today_date(), "%d %B %Y")
		return (date2 - date1).days
