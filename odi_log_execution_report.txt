# log_execution_report
# Author: Laercio Serra
# Created on: 10/07/2016
# Project: Push Notification
# Version 1: log executioin report to be send by e-mail

import string
import java.sql as sql
import java.lang as lang
import re
import time

sourceConnection = odiRef.getJDBCConnection("WORKREP")

# LINUX
# output_write=open('/u01/integracao/PUSHNOTIFICATION/log/Execution_Report_<%=odiRef.getSession("SESS_NO")%>.out','w')

output_write=open('/u01/integracao/MDM/log/Execution_Report_<%=odiRef.getSession("SESS_NO")%>.out','w')
#output_write=open('/u01/integracao/MDM/log/Execution_Report.out','w')

sqlstring = sourceConnection.createStatement()
localtime = time.asctime( time.localtime(time.time()) )

print >> output_write, "/*------------------------------------------------------------------------------------------------------------------------------------------------*/\n"
print >> output_write,'%s\n' % (str('  Execution Report for scenario : '+'<%=odiRef.getSession("SESS_NAME")%>'+'  ( '+localtime+' ) ').upper().center(124))
print >> output_write, "/*------------------------------------------------------------------------------------------------------------------------------------------------*/\n"

sqlstmt="
		select rownum, \
	       	sess.sess_no, \
	       	sess.sess_name, \
	       	step_log.nno, \
	       	step.step_name, \
	       	case when step.step_type='F' THEN 'Interface' \
	            when step.step_type='VD' THEN 'Variable declaration' \
	            when step.step_type='VS' THEN 'Set//Increment variable' \
	            when step.step_type='VE' THEN 'Evaluate variable' \
	            when step.step_type='V' THEN 'Refresh variable '\
	            when step.step_type='T' THEN 'Procedure' \
	            when step.step_type='OE' THEN 'OS command' \
	            when step.step_type='SE' THEN 'ODI Tool' \
	            when step.step_type='RM' THEN 'Reverse-engineer model' \
	            when step.step_type='CM' THEN 'Check model' \
	            when step.step_type='CS' THEN 'Check sub-model' \
	            when step.step_type='CD' THEN 'Check datastore' \
	            when step.step_type='JM' THEN 'Journalize model' \
	            when step.step_type='JD' THEN 'Journalize datastore' \
	            ELSE 'UNKNOWN' END as step_type, \
	      	to_char(step_log.step_beg,'DD-MON-YYYY HH24:MI:SS') as step_beg, \
	      	to_char(step_log.step_end,'DD-MON-YYYY HH24:MI:SS') as step_end, \
	      	step_log.step_dur, \
	      	case when step_log.step_status='D' THEN 'Success' \
	            when step_log.step_status='E' THEN 'Error' \
	            when step_log.step_status='Q' THEN 'Queued' \
	            when step_log.step_status='W' THEN 'Waiting' \
	            when step_log.step_status='M' THEN 'Warning' \
	            ELSE 'UNKNOWN' END as step_status, \
	      	step_log.nb_row, \
	      	step_log.nb_ins, \
	      	step_log.nb_upd, \
	      	step_log.nb_del, \
	      	step_log.nb_err, \
	     	dbms_lob.substr( TRANSLATE ( step_log.error_message, 'x'||CHR(10)||CHR(13), 'x'), 600, 1 )  as error_message \
		from snp_session sess 
				right outer join snp_sess_step step on sess.sess_no = step.sess_no \
        	    inner join snp_step_log step_log on step.sess_no = step_log.sess_no and step.nno = step_log.nno \
		where step_log.sess_no  = <%=odiRef.getSession("SESS_NO")%> \
      	order by step_log.nno"

print >> output_write, "StepNo StepName                                StepType            BeginningTime         EndTime               Duration   Status         Error_Msg\n"
print >> output_write, "------ --------------------------------------- ------------------- --------------------- --------------------- ---------- -------------- ----------\n"

result=sqlstring.executeQuery(sqlstmt)

while (result.next()):
    rownum=result.getInt("rownum")
    nno=result.getInt("nno")
    step_name=result.getString("step_name")
    step_type=result.getString("step_type")
    step_beg=result.getString("step_beg")
    step_end=result.getString("step_end")
    step_dur=result.getInt("step_dur")
    step_status=result.getString("step_status")
    error_message=result.getString("error_message")
    print >> output_write,'%7s%40s%20s%22s%22s%11s%15s%s\n' % (str(nno).ljust(7),step_name.ljust(40),step_type.ljust(20),str(step_beg).ljust(22),str(step_end).ljust(22),str(step_dur).ljust(11),step_status.ljust(15),str(error_message))

print >> output_write, "/*------------------------------------------------------------------------------------------------------------------------------------------------*/\n"
sourceConnection.close()
output_write.close() 
