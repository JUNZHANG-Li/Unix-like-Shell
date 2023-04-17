from applications.cat import cat, _cat
from applications.cd import cd, _cd
from applications.echo import echo, _echo
from applications.find import find, _find
from applications.grep import grep, _grep
from applications.head import head, _head
from applications.ls import ls, _ls
from applications.pwd import pwd, _pwd
from applications.tail import tail, _tail
from applications.cut import cut, _cut
from applications.uniq import uniq, _uniq
from applications.sort import sort, _sort
from applications.mkdir import mkdir, _mkdir
from applications.sed import sed, _sed
from applications.wc import wc, _wc
from applications.mv import mv, _mv
from applications.tsort import tsort, _tsort
from Errors.UnsupportedApplicationError import UnsupportedApplicationError


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs
            )
        return cls._instances[cls]


class App_Factory(metaclass=Singleton):
    def __init__(self) -> None:
        pass

    def create_application(self, application: str, args: list):

        applications = {
            "pwd": pwd,
            "cd": cd,
            "echo": echo,
            "ls": ls,
            "cat": cat,
            "head": head,
            "tail": tail,
            "grep": grep,
            "cut": cut,
            "find": find,
            "uniq": uniq,
            "sort": sort,
            "mkdir": mkdir,
            "sed": sed,
            "wc": wc,
            "mv": mv,
            "tsort": tsort,
        }

        unsafe_applications = {
            "_pwd": _pwd,
            "_cd": _cd,
            "_echo": _echo,
            "_ls": _ls,
            "_cat": _cat,
            "_head": _head,
            "_tail": _tail,
            "_grep": _grep,
            "_cut": _cut,
            "_find": _find,
            "_uniq": _uniq,
            "_sort": _sort,
            "_mkdir": _mkdir,
            "_sed": _sed,
            "_wc": _wc,
            "_mv": _mv,
            "_tsort": _tsort,
        }

        if application in applications:
            return applications[application](args)

        if application in unsafe_applications:
            return unsafe_applications[application](args)

        raise UnsupportedApplicationError(application)
