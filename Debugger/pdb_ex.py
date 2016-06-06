import sys
import pdb
from random import choice

random1 = [1,2,3,4,5,6,7,8,9,10,11,12]
random2 = [1,2,3,4,5,6,7,8,9,10,11,12]

while True:
	print "to exit this game type 'exit' "
	num1 = choice(random2)
	num2 = choice(random1)
	answer = raw_input("what is {} times {}? ".format(num1,num2))
	
	#pdb.set_trace()
	#exit
	if answer == 'exit':
		print "Now exiting game"
		sys.exit()
	
	#determine if number is correct
	
	elif int(answer) == num1 * num2:
		print "correct"
	else:
		print "wrong"