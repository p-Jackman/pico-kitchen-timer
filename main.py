import time
import tm1637
from machine import Pin

display = tm1637.TM1637(clk=Pin(26), dio=Pin(27))
reset_button = Pin(13, Pin.IN, Pin.PULL_DOWN)
seconds_up_button = Pin(12, Pin.IN, Pin.PULL_DOWN)
minutes_up_button = Pin(14, Pin.IN, Pin.PULL_DOWN)
restart_button = Pin(15, Pin.IN, Pin.PULL_DOWN)

#default time to start at, global variable storing current time in seconds
current_time = 600

seconds_counter = 0
minutes_counter = 0

start_time = time.time()

# current state: 0 = counting down, 1 = paused, 2 = end loop
state = 1


def update_display(raw_seconds):
    seconds = raw_seconds % 60
    minutes = (raw_seconds - seconds) / 60
    display.numbers(int(minutes), seconds)
    #print(str(int(minutes)) + ": " + str(seconds))    #comment out to not print out each time
    return    
    

def endloop():
    display.show(" end")
    time.sleep(0.75)
    display.show("    ")
    time.sleep(0.5)    
    return


# reset button interupt function
def interupt(Pin):
    global state
    
    if state == 0:
        state = 1
        
    elif state == 1:
        state = 0
        
    elif state == 2:
        state = 1
    print("state: " + str(state))
    time.sleep(0.25)
    return

reset_button.irq(trigger = Pin.IRQ_RISING, handler = interupt)


def seconds_up():
    global current_time
    global seconds_counter
    seconds_up = seconds_up_button.value()
    
    if seconds_up == True and seconds_counter <= 5:
        current_time = current_time + 1
        time.sleep(0.15)
        seconds_counter += 1
        print(seconds_counter)
    
    elif seconds_up == True and seconds_counter > 5:
        current_time = current_time + 1
        time.sleep(0.07)
    
    else:
        seconds_counter = 0
        
def minutes_up():
    global current_time
    global minutes_counter
    minutes_up = minutes_up_button.value()
    #print(minutes_up)
    
    if minutes_up == True and minutes_counter <= 5:
        current_time = current_time + 60
        time.sleep(0.25)
        minutes_counter += 1
        
#         print(seconds_counter)
    
    elif minutes_up == True and minutes_counter > 5:
        current_time = current_time + 60
        time.sleep(0.15)
    
    else:
        minutes_counter = 0


def restart_check():
    global current_time
    restart_value = restart_button.value()
    
    if restart_value == True:
        current_time = 0
        time.sleep(0.1)



if __name__ == '__main__':
    while True:
        if state == 0:
            #count(current_time, start_time, last_time)
            current_time = current_time - 1
            time.sleep(1)
            
            #timer is at 0, go to end state
            if current_time <= 0:
                state = 2
                
            #else show the time
            else:
                update_display(current_time)
        
        #paused state
        elif state == 1:
            update_display(current_time)
            seconds_up()
            minutes_up()
            restart_check()
            
            if current_time >= 5999:
                current_time = 5999
                
            #start_time = time.time()
        
        #end state
        elif state == 2:
            endloop()
            current_time = 600

