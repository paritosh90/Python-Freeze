import sys, inspect
class Freeze:
    def __init__(self, obj, arg):
        self.__dict__['obj'] = obj
        self.__dict__['list'] = arg if isinstance(arg,list) else []
        self.__dict__['list'].append('obj')
        self.__dict__['list'].append('list')

    def __repr__(self):
        return repr(self.obj)

    def __getattr__(self, item):
        self._test(item)
        return getattr(self.obj,item)

    def __setattr__(self, item, value):
        self._test(item)
        return setattr(self.obj, item, value)

    def _test(self, item):
        ##############################
        from datetime import datetime
        st=datetime.now()
        ##############################
        list = self.__dict__.get('list')
        list = list if list else []
        if item in list:
            frame = sys._getframe(2)
            arguments = frame.f_code.co_argcount
            if arguments is 0: raise Exception("%s is private variable of class %s"%(item,self.__class__.__name__))
            caller_calls_self = frame.f_code.co_varnames[0]
            thecaller = frame.f_locals[caller_calls_self]
            if item in list:
                if not id(self) == id(thecaller):
                    raise Exception("%s is private variable of class %s"%(item,self.__class__.__name__))
            ######################################
        en = datetime.now()
        print "Freeze: ",en-st

class Test:
    def __init__(self):
        self.item = 3

    def hello(self):
        self.item = 2

    def hi(self):
        from datetime import datetime
        a=datetime.now()
        print self.item
        b=datetime.now()
        print "Test: ",b-a