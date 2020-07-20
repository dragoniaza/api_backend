
from flask import Flask, request, jsonify, current_app, abort, send_from_directory, send_file, redirect
from flask_mysqldb import MySQL
import json
import requests

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'python_mysql'

mysql = MySQL(app)

# @app.route('/home')
# def home():
#     return "Hello World"
    
# @app.route('/addNewFavorite', methods=['POST'])
# def addNewFavorite():
#     print("addNewF")
#     dataInput = request.json
#     print("dataInput",dataInput)
#     user_id = dataInput['user_id']
#     file_name = dataInput['file_name']
#     conn = mysql.connection
#     cursor = conn.cursor()
#     sql_setUserFav = "INSERT INTO test_favorite (user_id,file_name) VALUES (%s,%s)"
#     cursor.execute(sql_setUserFav,(user_id,file_name))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     print("user_id:"+user_id+"\nfile_name:"+file_name)
#     print("")
#     return "Data has been save"

# @app.route('/removeFavorite', methods=['POST'])
# def removeFavorite():
#     dataInput = request.json
#     print(dataInput)
    
#     user_id = dataInput['user_id']
#     file_name = dataInput['file_name']
#     conn = mysql.connection
#     cursor = conn.cursor()
#     sql_setUserFav = "DELETE FROM test_favorite WHERE user_id = %s and file_name = %s"
#     cursor.execute(sql_setUserFav,(user_id,file_name))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return "Data has been delete"

def toJson(data,columns):
    results = []
    for row in data:
        results.append(dict(zip(columns, row)))
    return results

@app.route('/favoriteList', methods=['POST'])
def favoriteList():
    try:
        dataInput = request.json
        # print("dataInput",dataInput)
        if len(dataInput) == 0:
            # user_id = dataInput['user_id']
            # conn = mysql.connection
            # cursor = conn.cursor()
            return "Please log in before use this feature"
            
        else:
            user_id = dataInput['user_id']
            # print("user_id:",user_id)
            conn = mysql.connection
            cursor = conn.cursor()
            sql_getFavList = """SELECT export_excel.* FROM test_favorite JOIN export_excel ON export_excel.file_name = test_favorite.file_name
            WHERE export_excel.status = 'Active'
            and %s = test_favorite.user_id"""

            # sql_getFavList = """SELECT export_excel.* FROM test_favorite2 JOIN export_excel ON export_excel.file_name = test_favorite2.file_name
            # WHERE export_excel.status = 'Active'
            # and test_favorite2.status = 'Active'
            # and %s = test_favorite2.user_id"""


            # sql_getFavList = "SELECT * FROM test_favorite WHERE user_id = %s"
            cursor.execute(sql_getFavList,(user_id))
            data = cursor.fetchall()
            # print(data)
            columns = [column[0] for column in cursor.description]
            output = toJson(data, columns)
            conn.commit()
            # cursor.close()
            # conn.close()

            # return jsonify({"status": "200 is ok"})
            return jsonify({"result": output})  
    except Exception as e:
        current_app.logger.info(e)
        return jsonify({"status": "Error: " + str(e)})

# @app.route('/addNewFavorite2', methods=['POST'])
# def addNewFavorite2():
#     #get-input-data
#     dataInput = request.json
#     #get-value
#     user_id = dataInput['user_id']
#     #get-value
#     file_name = dataInput['file_name']
#     #connect-database
#     conn = mysql.connection
#     #prepare-for-quering
#     cursor = conn.cursor()
#     #query-with-search-data-in-db
#     # sql_getList = "SELECT user_id,file_name FROM test_favorite WHERE user_id = %s and file_name = %s"

#     sql_getList = "SELECT user_id,file_name FROM test_favorite2 WHERE user_id = %s and file_name = %s "

#     #submit-data
#     cursor.execute(sql_getList,(user_id,file_name))
#     #get-all-data
#     data = cursor.fetchall()
#     #store-in-(list)
#     columns = [column[0] for column in cursor.description]
#     #store-in-(json)
#     result_userAndFile = toJson(data, columns)

#     # print ("Data is : ")
#     # print (result_userAndFile)
#     # print ("Data Type is : " ,type(result_userAndFile))

#     #checking with length of data. if data hasn't some length. it's not store yet. we need to insert.BTW favorite
#     if len(result_userAndFile) != 0:
#         #Checking status after when api decide to change status active or inactive
#         sql_checkStatus = "SELECT status FROM test_favorite2 WHERE user_id = %s and file_name = %s and test_favorite2.status = 'Active'"
#         #execute SQL command 
#         cursor.execute(sql_checkStatus,(user_id,file_name))
#         #get data FROM SQL
#         data2 = cursor.fetchall()
#         #prepare data to JSON
#         columns = [column[0] for column in cursor.description]
#         #set data to JSON (custom JSON)
#         result_status = toJson(data2, columns)
#         # print("Check status of : user id =",user_id +" and file name = ",file_name +" status is : ",result_status)

#         #Checking lenght of JSON status file to decide which data must e active or inactive
#         if len(result_status) == 0:
#             #the data has not status active then change them to active
#             sql_setUserFav = "UPDATE test_favorite2 SET status = 'Active' WHERE user_id = %s and file_name = %s"
#             #execute SQL command
#             cursor.execute(sql_setUserFav,(user_id,file_name))
#             #submit SQL
#             conn.commit()
#         # print("Data has been delete")
#             return "1 : data has been change status to active"
#         else:
#             #the data is active by the way should be change to inactive
#             sql_setUserFav = "UPDATE test_favorite2 SET status = 'Inactive' WHERE user_id = %s and file_name = %s"
#             # sql_setUserFav = "DELETE FROM test_favorite WHERE user_id = %s and file_name = %s"
#             #execcute SQL command
#             cursor.execute(sql_setUserFav,(user_id,file_name))
#             #submit SQL
#             conn.commit()
#             return "0 : data has been change status to inactive"

#     #rechecking with length of data. if data has some length. it's already store in data. we need to remove them.BTW unfavorite
#     else :

#                 # print("Data has been insert")

#         #insert into database
#         sql_setUserFav = "INSERT INTO test_favorite2 (user_id,file_name,status) VALUES (%s,%s,'Active')"
#         # sql_setUserFav = "INSERT INTO test_favorite (user_id,file_name) VALUES (%s,%s)"
#         #insert with data input
#         cursor.execute(sql_setUserFav,(user_id,file_name))
#         #submit data
#         conn.commit()
#         return "1 : data has been insert"
        
#     cursor.close()
#     conn.close()
#     # return "Data has been save"
    
@app.route('/addNewFavorite', methods=['POST'])
def addNewFavorite():
    #get-input-data
    dataInput = request.json
    #get-value
    user_id = dataInput['user_id']
    #get-value
    file_name = dataInput['file_name']
    #connect-database
    conn = mysql.connection
    #prepare-for-quering
    cursor = conn.cursor()
    #query-with-search-data-in-db
    sql_getList = "SELECT user_id,file_name FROM test_favorite WHERE user_id = %s and file_name = %s"
    #submit-data
    cursor.execute(sql_getList,(user_id,file_name))
    #get-all-data
    data = cursor.fetchall()
    #store-in-(list)
    columns = [column[0] for column in cursor.description]
    #store-in-(json)
    result_userAndFile = toJson(data, columns)


    #checking with length of data. if data hasn't some length. it's not store yet. we need to insert.BTW favorite
    if len(result_userAndFile) == 0:
        #insert into database
        sql_setUserFav = "INSERT INTO test_favorite (user_id,file_name) VALUES (%s,%s)"
        #insert with data input
        cursor.execute(sql_setUserFav,(user_id,file_name))
        #submit data
        conn.commit()
        return True

    else :
        sql_setUserFav = "DELETE FROM test_favorite WHERE user_id = %s and file_name = %s"
        #execcute SQL command
        cursor.execute(sql_setUserFav,(user_id,file_name))
        #submit SQL
        conn.commit()
        return False

    cursor.close()
    conn.close()

if __name__ == "__main__":
    app.run(debug=True)