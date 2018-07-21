import pyclamd
import os
from blessings import Terminal

pyclamd.init_unix_socket('/var/run/clamd.scan/clamd.sock')


def av_scan_s3(tmpdir, bucket_name):
	av=[]
	t = Terminal()
	path=os.path.join(tmpdir, bucket_name)
	for subdir, dirs, files in os.walk(path):
		for file in files:
			subdir_path= os.path.join(path, subdir)
			file_path= os.path.join(subdir_path, file)
			av.append(pyclamd.scan_file(file_path))
			av=[x for x in av if x is not None]
			for n in range(len(av)):
                        	index_number= n
				if str(file_path) in av[n]:
					file= file_path
					virus= list(av[n][str(file_path)])
					virus.remove("FOUND")
					virus=str(virus)[2:-2]
					print t.red('Critical !')+ " I found "+virus+ " in the infected file "+file

