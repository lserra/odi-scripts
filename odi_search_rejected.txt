# search_rejected
# Author: Laercio Serra
# Created on: 10/07/2016
# Project: License Ticket
# Version 1: search the records rejects during the load and send a list by e-mail

<@
 
import java.sql.Connection;
import java.sql.Statement;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
 
conn=odiRef.getJDBCConnection("SRC");
Statement stmt=conn.createStatement();
String result="";
 
char delimiter=(char)44;

// Please change the delimiter here,i.e just change the number
// TAB - 9
// COMMA 44
// GET THE CODING LIST AT http://www.zytrax.com/tech/codes.htm
 
my_query="
	SELECT  
		ODI_ERR_MESS,
		PERS_DS_EMAIL,
		PERS_NM_NAME,
		CASE WHEN PERS_CD_SOURCEWKF='S' THEN 'WORKFORCE'
		WHEN PERS_CD_SOURCETCKT='S' THEN 'TICKETING'
		WHEN PERS_CD_SOURCELIC='S' THEN 'LICENSING'
		WHEN PERS_CD_SOURCENEWS='S' THEN 'NEWSLETTER'
		WHEN PERS_CD_SOURCETORCH='S' THEN 'TOCHA'
		WHEN PERS_CD_SOURCEEDU='S' THEN 'EDUCAÇÃO' END AS ORIGEM
	FROM E$_PERSON ";
 
// Either provide the columns or select * from all columns
 
ResultSet rs=stmt.executeQuery(my_query);
ResultSetMetaData md=rs.getMetaData();
int numColumns =md.getColumnCount();
 
// Fetch column names
for (int i=1; i<numColumns+1; i++) {
 String columnName = md.getColumnName(i)+ delimiter;
 result+=columnName;
 }
 
result=result.substring(0,result.length()-1);
result+=(char)10;
 
int times=result.length();
 
for (int i=1; i<times ;i++){
 result+="-";
 }
 
result+=(char)10;
 
// Fetching Rows
 
result=result.substring(0,result.length()-1);
result+=(char)10;
 
while (rs.next()) {
 for (int i=1; i<numColumns+1; i++) {
 String  output=rs.getString(md.getColumnName(i))+ delimiter;
 result+=output;
 }
result=result.substring(0,result.length()-1);   
result+=(char)10;
 }
 
// Close Connection
 
stmt.close();
conn.close();
@>