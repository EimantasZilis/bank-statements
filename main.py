import statements
import plot.monthly
import plot.summary


print('Generating plots...')
plot.monthly.do_it(statements.data)
plot.summary.do_it(statements.data)
