class Deletecars:
   def delete_task(db, id):
      with utilsObj.connection.cursor() as db:
      """
      Delete a task by task id
      :param conn:  Connection to the SQLite databas
      :param id: id of the task
      :return:
      """
      sql = 'DELETE FROM tasks WHERE id=?'
      cursor = db.cursor()
      cursor.execute(sql, (id,))
      conn.commit()