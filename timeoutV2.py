import signal

class TimeoutException(Exception):
    """A timeout has occurred."""
    pass

def timeout(t):
    print "timeout = " + str(t)
    def wrap(f):
        print "fun = " + str(f)
        def handler(signum, frame): 
            raise TimeoutException()
        def wrapped_f(*args):
            print "in wrapped_f"
            old = signal.signal(signal.SIGALRM, handler) 
            # set the alarm
            signal.alarm(t) 
            try: 
                result = f(*args)
            finally: 
                # restore existing SIGALRM handler
                signal.signal(signal.SIGALRM, old)
            signal.alarm(0)
            return result 
        return wrapped_f
    return wrap
