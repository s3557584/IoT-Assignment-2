from DatabaseUtil import DatabaseUtil
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

utilsObj = DatabaseUtil()
class Deletecars:
   def delete_task(db, id):
      dele = 0
      with utilsObj.connection.cursor() as db:
      """
      Delete a task by task id
      :param conn:  Connection to the SQLite databas
      :param id: id of the task
      :return:
      """
      if cursor.dele():
         print("Do you want to delete your booking?")
         sql = 'DELETE FROM tasks WHERE id=?'
         cursor = db.cursor()
         cursor.execute(sql, (id,))
         conn.commit()
      else
      dele = 1