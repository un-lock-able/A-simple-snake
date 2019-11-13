import pyHook as hook
from random import randint
from multiprocessing import Process,Manager
import os,win32gui,time,pythoncom
windowhandle = win32gui.GetForegroundWindow()
settings= {
	'width':20,
	'height':20,
	'sleeptime':0.3
}
score = 0
wide = settings['width']
hight = settings['height']
maxscore = int(wide*hight/20)
applepos = (int(wide/2),int(hight/2))
snake=[(int(wide/2),int(hight/2+1)),(int(wide/2),int(hight/2))]
#these datas are in the format of x,y
'''
left = 1
up = 2
right = 3
down = 4
██░░
'''
def hooking():
	hm = hook.HookManager()
	hm.KeyDown = keyboard
	hm.HookKeyboard()
	pythoncom.PumpMessages()

def keyboard(event):
	#if event.Window == windowhandle and event.KeyID>=37 and event.KeyID<=40:
	global windowhandle
	fl = open('direction.temp','w')
	if (event.Window == windowhandle and event.KeyID>=37 and event.KeyID<=40):
		#print('get')
		fl.write(str(int(event.KeyID)-36))
	elif (event.Window == windowhandle and event.Key == 'Numpad0'):
		fl.write('pause')
	fl.close()
	return True

def display():
	global score,nextscore
	os.system('cls')
	print('')
	for i in range(0,hight):
		print('  ',end = '')
		for j in range(0,wide):
			print(screen[i][j],end = '')
		print('')
	print('Scores: %d    Next score: %d'%(score,nextscore),end = '', flush = True)

def makescreen():
	for i in range(0,hight):
		line = []
		for j in range(0,wide):
			line.append('░░')
		screen.append(line)

def makeapple():
	global applepos
	while applepos in snake:
		applepos = (randint(0,wide-1),randint(0,hight-1))
	screen[applepos[1]][applepos[0]]='  '
	#when applying to screen, use format of y,x

def movesnake(direction):
	global score,nextscore
	if direction == 1:#left
		if snake[-1][0]-1 < 0:
			nextstep = (snake[-1][0]-1+wide,snake[-1][1])
		else:
			nextstep = (snake[-1][0]-1,snake[-1][1])
		if nextstep == snake[-2]:
			return movesnake(3)
	elif direction == 2:#up
		if snake[-1][1]-1 < 0:
			nextstep = (snake[-1][0],snake[-1][1]-1+hight)
		else:
			nextstep = (snake[-1][0],snake[-1][1]-1)
		if nextstep == snake[-2]:
			return movesnake(4)
	elif direction == 3:#right
		if snake[-1][0]+1 > wide-1:
			nextstep = (snake[-1][0]+1-wide,snake[-1][1])
		else:
			nextstep = (snake[-1][0]+1,snake[-1][1])
		if nextstep == snake[-2]:
			return movesnake(1)
	elif direction == 4:#down
		if snake[-1][1]+1 > hight - 1:
			nextstep = (snake[-1][0],snake[-1][1]+1-hight)
		else:
			nextstep = (snake[-1][0],snake[-1][1]+1)
		if nextstep == snake[-2]:
			return movesnake(2)
	if nextstep in snake[:-2]:
		return False
	snake.append(nextstep)
	screen[nextstep[1]][nextstep[0]]='\033[0;32;40m██\033[0m'
	screen[snake[-2][1]][snake[-2][0]] = '██'
	if nextstep != applepos:
		screen[snake[0][1]][snake[0][0]]='░░'
		del snake[0]
		if nextscore != 1:
			nextscore-=1
	else:
		makeapple()
		score+=nextscore
		nextscore = maxscore
	return True


if __name__ == '__main__':
	moni = Process(target = hooking,args = ())
	moni.start()
	screen = []
	makescreen()
	screen[int(hight/2)][int(wide/2)]='\033[0;32;40m██\033[0m'
	screen[int(hight/2+1)][int(wide/2)]='██'
	makeapple()
	fl = open('direction.temp','w')
	fl.write('2')
	fl.close()
	alive = True
	nextscore = maxscore
	while alive:
		display()
		time.sleep(settings['sleeptime'])
		with open('direction.temp','r') as fl:
			direction=fl.readlines()[0]
			if direction == 'pause':
				print('')
				os.system('pause')
			else:
				direction = int(direction)
				alive = movesnake(direction)
	moni.terminate()
	os.remove('direction.temp')
	os.system('pause')
