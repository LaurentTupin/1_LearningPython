

def Draft():
    
    
    try:
        int_unit = 5 / 0
    except Exception as err:
        print(err)
   

    try:
        int_unit = 'a' + 5
    except ZeroDivisionError as err:
        print('ZeroDivisionError: ', err)
        # --> ZeroDivisionError:  division by zero
    except Exception as err:
        print('Other error: ', err)
        # --> Other error:  can only concatenate str (not "int") to str
    else:
        print('No error')
        print(int_unit)
    finally:
        print('Going there if there is an error or not')
        
    
    
Draft()

	
	
