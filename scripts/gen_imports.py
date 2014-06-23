#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: {}
"""
Some Python code generators
"""
__author__ = 'rockyroad'

class ImportsGenerator():
    """
    Collects used classes and generates needed import lines.

    .. todo:: generate forms for several or all model in a given module.
    """
    imports = {}
    names = []

    def add_obj(self, obj):
        return self.add_class(obj.__class__)

    def add_class(self, the_class):
        #print "adding ", str(the_class)
        mod = str(the_class.__module__)
        name = the_class.__name__
        if name in self.names:
            raise Exception("Name conflict for %s, can't import from %s ", name, mod)
        if mod in self.imports:
            if name not in self.imports[mod]:
                self.imports[mod] += [name]
        else:
            self.imports[mod] = [name]

    def python(self):
        """
        Produces python import lines for collected classes.
        """
        code = ''
        for mod, imps in self.imports.iteritems():
            code += "from {0} import {1}\n".format(mod, ', '.join(imps))
        return code


def run():
    """
    Does great things.
    """
    gen = ImportsGenerator()
    from wtforms.ext.sqlalchemy.fields import QuerySelectField
    gen.add_class(QuerySelectField)
    import wtforms
    gen.add_class(wtforms.fields.simple.TextField)
    gen.add_class(wtforms.fields.simple.PasswordField)
    gen.add_class(wtforms.fields.DateTimeField)
    gen.add_class(wtforms.fields.FieldList)
    print gen.python()

if __name__ == '__main__':
    run()
