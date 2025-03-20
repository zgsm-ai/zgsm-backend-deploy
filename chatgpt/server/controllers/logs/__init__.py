 # -*- coding: utf-8 -*-
 import datetime
 
 # The class of time tool
 class TimeTool:
 
  # Get current time string
  # Format: YYYY-MM-DD HH:MM:SS
  @staticmethod
  def get_now_string():
   return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
 
  # Get current date string
  # Format: YYYY-MM-DD
  @staticmethod
  def get_today_string():
   return datetime.datetime.now().strftime('%Y-%m-%d')
 
  # Convert time string to timestamp
  # time_string: Time string, format: YYYY-MM-DD HH:MM:SS
  # return: Timestamp
  @staticmethod
  def string_to_timestamp(time_string):
   time_tuple = datetime.datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")
   timestamp = time.mktime(time_tuple.timetuple())
   return timestamp
 
  # Convert timestamp to time string
  # timestamp: Timestamp
  # return: Time string, format: YYYY-MM-DD HH:MM:SS
  @staticmethod
  def timestamp_to_string(timestamp):
   time_tuple = time.localtime(timestamp)
   time_string = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)
   return time_string
 ```
 ```python
 # -*- coding: utf-8 -*-
 import datetime
 
 # The class of time tool
 class TimeTool:
 
  # Get current time string
  # Format: YYYY-MM-DD HH:MM:SS
  @staticmethod
  def get_now_string():
   return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
 
  # Get current date string
  # Format: YYYY-MM-DD
  @staticmethod
  def get_today_string():
   return datetime.datetime.now().strftime('%Y-%m-%d')
 
  # Convert time string to timestamp
  # time_string: Time string, format: YYYY-MM-DD HH:MM:SS
  # return: Timestamp
  @staticmethod
  def string_to_timestamp(time_string):
   time_tuple = datetime.datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")
   timestamp = time.mktime(time_tuple.timetuple())
   return timestamp
 
  # Convert timestamp to time string
  # timestamp: Timestamp
  # return: Time string, format: YYYY-MM-DD HH:MM:SS
  @staticmethod
  def timestamp_to_string(timestamp):
   time_tuple = time.localtime(timestamp)
   time_string = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)
   return time_string
 ```