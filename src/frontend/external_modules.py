# https://stackoverflow.com/questions/3349157/python-passing-a-function-name-as-an-argument-in-a-function
class Call(object):
  def __init__(self, name):
    self.n, self.f = name, None

  def __call__(self, *a, **k):
    if self.f is None:
      modn, funcn = self.n.rsplit('.', 1)
      if modn not in sys.modules:
        __import__(modn)
      self.f = getattr(sys.modules[modn],
                       funcn)
    self.f(*a, **k)