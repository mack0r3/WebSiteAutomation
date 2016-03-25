from ftplib import FTP

ftp = FTP('ftp.caya.nazwa.pl')
ftp.login("caya_collection", "GoscFtp14")
ftp.cwd('Costa')

files = ftp.nlst()

counter = 0
for file in files:
	counter += 1
	print (str(counter) + "#" + file[0])
