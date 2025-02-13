# book_data = [{'id': 1, 'books_title': 'Let us Python', 'author': 'Yaswant Kanetkar', 'genre': 'programming',
#               'published_date': '2019-07-08', 'available_copies': 10}]
# print(book_data[0]['available_copies']-1)

# from Library_Backend_Api.date_time_module import get_today_date, date_after_15_days
#
# print(get_today_date())
# print(date_after_15_days())

# from datetime import datetime, timedelta
#
# # Given date string
# date_str = "09 February 2025"
#
# # Convert string to datetime object
# date_obj = datetime.strptime(date_str, "%d %B %Y")
#
# # Add 15 days
# new_date = date_obj + timedelta(days=15)
#
# # Convert back to string (if needed)
# new_date_str = new_date.strftime("%d %B %Y")
#
# print(f"New date after adding 15 days: {new_date_str}")
# fine = 00
# response_message = {"message": "Deleted successfully"}
# if fine > 0:
# 	response_message["fine"] = f"{fine}₹ fine"
# 	print(response_message)
# print(response_message)

for i in range(5):
	for j in range(i):
		print("*",end='')
	print()


