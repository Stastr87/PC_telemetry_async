import os
import shutil
import weakref

class FileRemover(object):
    def __init__(self):
        self.weak_references = dict()  # weak_ref -> filepath to remove

    def cleanup_once_done(self, response, filepath):
        wr = weakref.ref(response, self._do_cleanup)
        self.weak_references[wr] = filepath

    def _do_cleanup(self, wr):
        filepath = self.weak_references[wr]
        if os.path.isfile(filepath):
            with open(filepath, 'w') as file:
                file.write('TTTTTTTTTT')
        print('Deleting %s' % filepath)
        # shutil.rmtree(filepath, ignore_errors=True)
        # os.remove(filepath)
        os.unlink(filepath)