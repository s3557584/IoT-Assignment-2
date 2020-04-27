class Deletecars
  def delete_task(db, id)：
   sql = 'DELETE FROM tasks WHERE id=?'
    cursor = db.cursor()
    cursor.execute(sql, (id,))
    conn.commit()