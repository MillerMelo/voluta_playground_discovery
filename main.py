import pyb
from pyb import Pin, Timer, ExtInt


in_btn_play 	= Pin('PB12', Pin.IN)
in_btn_home 	= Pin('PB13', Pin.IN)
in_btn_pos_0 	= Pin('PB14', Pin.IN)
in_home_x 		= Pin('PC6', Pin.IN)
in_home_y 		= Pin('PC7', Pin.IN)
in_home_z 		= Pin('PB8', Pin.IN)

out_pwm_x 		= Pin('PA3', Pin.OUT_PP)
out_pwm_y 		= Pin('PA1', Pin.OUT_PP)
out_pwm_z 		= Pin('PA2', Pin.OUT_PP)
out_dir_x 		= Pin('PE1', Pin.OUT_PP)
out_dir_y 		= Pin('PE2', Pin.OUT_PP)
out_dir_z 		= Pin('PE3', Pin.OUT_PP)
out_enable_x	= Pin('PE4', Pin.OUT_PP)
out_enable_y	= Pin('PE5', Pin.OUT_PP)
out_enable_z	= Pin('PE6', Pin.OUT_PP)

run_home_x 		= False
run_home_y 		= False
run_home_z 		= False
home_x_ok 		= False
home_y_ok 		= False
home_z_ok 		= False



def home_x():
	out_enable_x.low()
	out_dir_x.high()
	pwm_ch_x = pwm_eje_x.channel(4, Timer.PWM, pin=out_pwm_x)
	pwm_ch_x.pulse_width_percent(50)
	print("Run Home X")

def home_z():
	out_enable_z.low()
	out_dir_z.low()
	pwm_ch_z = pwm_eje_z.channel(3, Timer.PWM, pin=out_pwm_z)
	pwm_ch_z.pulse_width_percent(50)
	print("Run Home Z")


def irq_home_x(line):
	global run_home_x, home_x_ok
	
	if run_home_x:
		pwm_eje_x.deinit()
		run_home_x = False
		home_x_ok = True
		print("Home X OK")

def irq_home_z(line):
	global run_home_z, home_z_ok
	
	if run_home_z:
		pwm_eje_z.deinit()
		run_home_z = False
		home_z_ok = True
		print("Home Z OK")




pwm_eje_x = Timer(5, freq=400)
pwm_eje_z = Timer(2, freq=400)

conf_in_home_x = ExtInt(in_home_x, ExtInt.IRQ_FALLING, Pin.PULL_UP,irq_home_x)
conf_in_home_z = ExtInt(in_home_z, ExtInt.IRQ_FALLING, Pin.PULL_UP,irq_home_z)

out_enable_x.high()
out_enable_y.high()
out_enable_z.high()


while True:

	if in_btn_home.value():

		if not in_home_z.value():
			if not home_z_ok:
				home_z_ok = True
				print("Home Z OK")
		else:
			if not run_home_z:
				run_home_z = True
				home_z()

	if home_z_ok and not home_x_ok:
		if not run_home_x:
			run_home_x = True
			home_x()



	if in_btn_play.value():
		pass

	if in_btn_pos_0.value():
		pass


