__author__="gmcwhirt"
__date__ ="$Sep 27, 2011 4:23:03 PM$"

from abc import ABCMeta
from abc import abstractmethod
from optparse import OptionParser

effective_zero_diff = 1e-11
effective_zero = 1e-10

class Simulation:
    __metaclass__ = ABCMeta

    def __init__(self):
        self._oparser = OptionParser()
        self._options = None
        self._args = None
        self._data = {}
        self._setBaseParserOptions()
        self._setParserOptions()

    def go(self):
        (self._options, self._args) = self._oparser.parse_args()
        self._checkParserOptions()
        self._setData()

        output_base = "{0}/{1}".format(self._options.output_dir, "{0}")

        stats = open(output_base.format(self._options.stats_file), "wb")

        pool = mp.Pool(self._options.pool_size)
        if not self._options.quiet:
            print "Pool: {0}".format(pool)

        mp.log_to_stderr()

        if not options.quiet:
            print "Running {0} duplications.".format(self._options.dup)

        task_base = self._buildTask()
        if self._options.file_dump:
            tasks = [tuple(task_base + [output_base.format(self._options.output_file.format(i + 1)), self._options.skip]) for i in range(self._options.dup)]
        else:
            tasks = [tuple(task_base + [None, self._options.skip, self._options.quiet])] * self._options.dup

        results = pool.imap_unordered(self.runSimulationIMap, tasks)
        finished_count = 0
        for result in results:
            finished_count += 1
            if not options.quiet:
                print self._outputRun(result)
            print >>stats, cPickle.dumps(result)
            print >>stats
            stats.flush()
            print "done #{0}".format(finished_count)

        stats.close()

    def runSimulationIMap(self, args):
        return self.runSimulation(*args)

    def _setBaseParserOptions(self):
        self._oparser.add_option("-d", "--duplications", type="int", action="store", dest="dup", default=1, help="number of duplications")
        self._oparser.add_option("-o", "--output", action="store", dest="output_dir", default="./output", help="directory to dump output files")
        self._oparser.add_option("-f", "--filename", action="store", dest="output_file", default="duplication_{0}", help="output file name template")
        self._oparser.add_option("-g", "--nofiledump", action="store_false", dest="file_dump", default=True, help="do not output duplication files")
        self._oparser.add_option("-k", "--skip", action="store", type="int", dest="skip", default=1, help="number of generations between dumping output -- 0 for only at the end")
        self._oparser.add_option("-s", "--statsfile", action="store", dest="stats_file", default="aggregate", help="file for aggregate stats to be dumped")
        self._oparser.add_option("-m", "--poolsize", action="store", type="int", dest="pool_size", default=2, help="number of parallel computations to undertake")
        self._oparser.add_option("-q", "--quiet", action="store_true", dest="quiet", default=False, help="suppress standard output")

    def _formatRun(self, result):
        return result

    def _setParserOptions(self):
        pass

    def _checkParserOptions(self):
        pass

    def _setData(self):
        pass

    @abstractmethod
    def _buildTask(self):
        return []

    @abstractmethod
    @classmethod
    def runSimulation(cls):
        pass


