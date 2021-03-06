
from Client import send 		#email capabilites are imported from Client.py
import datetime
import sys
import glob


keyword = 'TrapRestorerWorker' # <-- This is where you enter the keyword to be searched
count = 0
LastLine=''  	

def get_last_date():							#TimeStamps
    try:				#need the try and except method because when the last_date.txt doesn't exist it will automatically create the last_date.txt with the date and time of 1990-01-01 00:00:00 000000
        with open('last_date.txt') as last_date_file:	
            last_date_str = last_date_file.read().strip()
            return datetime.datetime.strptime(last_date_str, '%Y-%m-%d %H:%M:%S %f')
    except IOError:

        return datetime.datetime.strptime('1990-01-01 00:00:00 000000', '%Y-%m-%d %H:%M:%S %f')


def set_last_date(t):						   

    with open('last_date.txt', 'w') as last_date_file:
        last_date_str = t.strftime('%Y-%m-%d %H:%M:%S %f')
        last_date_file.write(last_date_str)


t0 = get_last_date()

for logpath in glob.glob('/opt/5620sam/server/nms/log/server/EmsServer.log'): #The path of the file to be searched can be entered here
    #print ('logpath:',logpath)
    with open(logpath, 'r') as logfile:
        for line in logfile.readlines():
            line = line.strip()
            if line.startswith('<'):											#If the line startswith '<' then that line is read or else it skips
                datepart,_,_ = line.partition('>')								#The line is partioned at the first encounter of '>' and then the left side of the line is stored in variable datapart
                datepart = datepart[1:]
                                                                                #the lines would look something like <2016.10.24 13:00 4000 ET> Keyword ........
                date, time, ms, tz = datepart.split(' ')						#split datepart as date, time, ms , tz

                year,month,day = date.split('.')								#Date and time is split in respect with how they are represented in the list
                hour,minute,second = time.split(':')							

                year,month,day = int(year), int(month), int(day)			
                hour,minute,second = int(hour), int(minute), int(second)
                ms = long(ms)

                t = datetime.datetime(year=year, month=month, day=day			#The datetime is stored in the variable t
                                , hour=hour, minute=minute, second=second	 
                                , microsecond=ms*1000.0,tzinfo=None)
            if t < t0:
                continue

            count += line.count(keyword)
            set_last_date(t)
            if keyword in line:
                message1 = 'Counted %s %s times in %s line' % (repr(keyword), count, line)
                LastLine=line
                #print message1 			#for Test
if (count==0):																	#if count is0 no email is sent
    exit()
message = """The script /opt/5620sam/server/nms/bin/unsupported/checkEMSforText.py found the key word %s in EMS logs %s times.\n *** Last Ems Log Message***:: \n %s"""  % (repr(keyword), count,LastLine) #Body of the mail can be edited here.
print message		#for Test
message2= '\n Last Ems Log Message:\n %s' %(LastLine)
#print message2		#for Test
send('adithya.rathakrishnan@nokia.com','5620 SAM: EMS logs report message that there may be an issue with the Aux servers',message,'<div>%s</div>' % message) # Email "to" address should be added in the first argument here
#need the fourth argument to be html format for the Mail to be dispalyed properly */


