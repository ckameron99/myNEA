import cProfile
import main
import pstats
cProfile.run("main.main()","runtime.info")
p=pstats.Stats("runstats")
p.strip_dirs().sort_stats("cumtime")
p.print_stats()
