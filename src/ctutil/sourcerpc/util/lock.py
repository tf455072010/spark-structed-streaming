
def auto_shared_lock(mutext_lock):
    '''
    自动加锁和释放锁
    '''

    def __autolock(func):
        def __lockmethod(*args, **kwargs):
            if mutext_lock:
                mutext_lock.acquire()
            try:
                return func(*args, **kwargs)
            finally:
                if mutext_lock:
                    mutext_lock.release()

        return __lockmethod

    return __autolock
