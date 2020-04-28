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